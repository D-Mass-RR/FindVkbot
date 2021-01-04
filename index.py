import telebot
import os
from telebot import types

MainPath = r"C:\Users\123\PycharmProjects\FindVk\users"

# def saveData(path, data, type):
#     with open()

def checText(text):
    try:
        return {
            "привет" : "соси хуй"
        }[text]
    except: return "атсаси"

#передаем наш токен бота
bot = telebot.TeleBot("1496934915:AAFEMM4mxh3SyYO6hazmq2WK2ORQxcyT3vA")

#commands обрабатывает команды, которые передает пользователь
@bot.message_handler(commands=["start"])
def start(message):
    src = MainPath + f"\\{message.from_user.first_name}_{message.chat.id}"
    if os.path.exists(src) == False:
        os.mkdir(src)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("найти по фотке")
    markup.add(btn1)

    #massege передает декоратор
    sendMessage = f"привет {message.from_user.first_name }!"
    bot.send_message(message.chat.id, sendMessage, reply_markup=markup)
    bot.send_message(message.chat.id, "Что хочешь сделать?")

@bot.message_handler(content_types=["text"])
def findUser(message):
    if message.text.strip().lower() == "найти по фотке":
        bot.send_message(message.chat.id, "нажми 'поделиться контактом'")

@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None: #Если присланный объект <strong>contact</strong> не равен нулю
        phoneNumber = message.contact.phone_number
        src = MainPath + f"\\{message.from_user.first_name}_{message.chat.id}\\data.json"
        with open(src, "w") as data:
            data.write("phoneNuber:" + phoneNumber)


@bot.message_handler(content_types=["document"])
def handle_docs_photo(message):
    try:
        bot.reply_to(message, "спасибо")

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = MainPath + f"\\{message.from_user.first_name}_{message.chat.id}" + "\\" + str(message.document.file_id) + ".jpg"
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)

    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(content_types=["text"])
def mess(message):
    getMessage = message.text.strip().lower()
    try:

        src = MainPath + f"\\{message.from_user.first_name}_{message.chat.id}\\messages.txt"
        with open(src, "a") as savedMessage:
            savedMessage.write(getMessage + "\n")
        outputMessage = checText(getMessage)
        bot.send_message(message.chat.id, outputMessage)
    except UnicodeEncodeError:
        pass

#этот метод нужен что бы бот не отключался
bot.polling(none_stop=True)
