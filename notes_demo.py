import vk_api
import os
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

bot_token = ""


def main():
    vk_session = vk_api.VkApi(token=bot_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('help', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('add', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('show', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('edit', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('rename', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('delete', color=VkKeyboardColor.DEFAULT)

    add = {}
    show = {}
    edit = {}
    rename = {}
    delete = {}
    file_names = {}

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print('id{}: "{}"'.format(event.user_id, event.text), end='\n')
            try:
                if event.text.lower() == "help":
                    response = "help - просмотреть доступные для ввода команды.\n"
                    response += "add - добавить новую заметку.\n"
                    response += "show - показать текущие заметки.\n"
                    response += "edit - редактировать заметку.\n"
                    response += "rename - переименовать заметку.\n"
                    response += "delete - удалить заметку.\n"
                    add[event.user_id] = 0
                    show[event.user_id] = 0
                    edit[event.user_id] = 0
                    rename[event.user_id] = 0
                    delete[event.user_id] = 0
                elif event.text.lower() == "show":
                    response = "Введите заголовок заметки которую хотите просмотреть:\n\n"
                    this_dir = os.getcwd()
                    for root, directories, files in os.walk(this_dir):
                        for f in files:
                            if str(event.user_id) in f:
                                response += f[len(str(event.user_id))+1:-4] + "\n"
                    if response == "Введите заголовок заметки которую хотите просмотреть:\n\n":
                        response = "У вас нет ни одной заметки."
                    add[event.user_id] = 0
                    show[event.user_id] = 1
                    edit[event.user_id] = 0
                    rename[event.user_id] = 0
                    delete[event.user_id] = 0
                elif event.text.lower() == "add":
                    response = "Введите заголовок для новой заметки:"
                    add[event.user_id] = 1
                    show[event.user_id] = 0
                    edit[event.user_id] = 0
                    rename[event.user_id] = 0
                    delete[event.user_id] = 0
                elif event.text.lower() == "edit":
                    response = "Введите заголовок заметки которую хотите редактировать:\n\n"
                    this_dir = os.getcwd()
                    for root, directories, files in os.walk(this_dir):
                        for f in files:
                            if str(event.user_id) in f:
                                response += f[len(str(event.user_id))+1:-4] + "\n"
                    if response == "Введите заголовок заметки которую хотите редактировать:\n\n":
                        response = "У вас нет ни одной заметки."
                    add[event.user_id] = 0
                    show[event.user_id] = 0
                    edit[event.user_id] = 1
                    rename[event.user_id] = 0
                    delete[event.user_id] = 0
                elif event.text.lower() == "rename":
                    response = "Введите заголовок заметки которую хотите переименовать:\n\n"
                    this_dir = os.getcwd()
                    for root, directories, files in os.walk(this_dir):
                        for f in files:
                            if str(event.user_id) in f:
                                response += f[len(str(event.user_id))+1:-4] + "\n"
                    if response == "Введите заголовок заметки которую хотите переименовать:\n\n":
                        response = "У вас нет ни одной заметки."
                    add[event.user_id] = 0
                    show[event.user_id] = 0
                    edit[event.user_id] = 0
                    rename[event.user_id] = 1
                    delete[event.user_id] = 0
                elif event.text.lower() == "delete":
                    response = "Введите заголовок заметки которую хотите удалить:\n\n"
                    this_dir = os.getcwd()
                    for root, directories, files in os.walk(this_dir):
                        for f in files:
                            if str(event.user_id) in f:
                                response += f[len(str(event.user_id))+1:-4] + "\n"
                    if response == "Введите заголовок заметки которую хотите удалить:\n\n":
                        response = "У вас нет ни одной заметки."
                    add[event.user_id] = 0
                    show[event.user_id] = 0
                    edit[event.user_id] = 0
                    rename[event.user_id] = 0
                    delete[event.user_id] = 1

                elif delete[event.user_id] == 1:
                    os.remove(str(event.user_id) + "_" + event.text + ".txt")
                    response = "Заметка успешно удалена."
                    delete[event.user_id] = 0
                elif rename[event.user_id] == 1:
                    file_names[event.user_id] = str(event.user_id) + "_" + event.text + ".txt"
                    response = "Заметки с таким именем не существует. Поробуйте ввести имя еще раз:"
                    rename[event.user_id] = 1
                    this_dir = os.getcwd()
                    for root, directories, files in os.walk(this_dir):
                        for f in files:
                            if str(event.user_id) in f:
                                if event.text == f[len(str(event.user_id))+1:-4]:
                                   response = "Введите новый заголовок для этой заметки:"
                                   rename[event.user_id] = 2
                elif rename[event.user_id] == 2:
                    os.rename(file_names[event.user_id], str(event.user_id) + "_" + event.text + ".txt")
                    response = "Заметка успешно переименована."
                    rename[event.user_id] = 0
                elif edit[event.user_id] == 1:
                    file_names[event.user_id] = str(event.user_id) + "_" + event.text + ".txt"
                    with open(file_names[event.user_id], "r") as file_obj:
                        response = file_obj.read()
                    response1 = "Скопируйте текст заметки, отредактируйте и отправьте новый вариант."
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=response1,
                    )
                    edit[event.user_id] = 2
                elif edit[event.user_id] == 2:
                    with open(file_names[event.user_id], "w") as file_obj:
                        file_obj.write(event.text)
                    response = "Заметка успешно сохранена."
                    edit[event.user_id] = 0
                elif add[event.user_id] == 1:
                    file_names[event.user_id] = str(event.user_id) + "_" + event.text + ".txt"
                    response = "Введите текст новой заметки:"
                    add[event.user_id] = 2
                elif add[event.user_id] == 2:
                    with open(file_names[event.user_id], "w") as file_obj:
                        file_obj.write(event.text)
                    response = "Заметка успешно сохранена."
                    add[event.user_id] = 0
                elif show[event.user_id] == 1:
                    with open(str(event.user_id) + "_" + event.text + ".txt", "r") as file_obj:
                        response = file_obj.read()
                    show[event.user_id] = 0
                else:
                    response = "Ошибка ввода. Отправьте 'help' чтобы просмотреть все доступные команды."

            except Exception as e:
                print(e)
                response = "Ошибка ввода. Отправьте 'help' чтобы просмотреть все доступные команды."
                add[event.user_id] = 0
                show[event.user_id] = 0
                edit[event.user_id] = 0
                rename[event.user_id] = 0
                delete[event.user_id] = 0

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=response,
                keyboard=keyboard.get_keyboard(),
            )


if __name__ == '__main__':
    main()


