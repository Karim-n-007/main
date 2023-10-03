import os
import cv2
import random
import string
import socket
import telebot
import smtplib
import mimetypes
import pyautogui
from time import sleep
from telebot import types
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Generating a new password to log in to the bot every new launch
def generate_password():
    def randomize_password(password):
        password_list = list(password)
        random.shuffle(password_list)
        return "".join(password_list)
    number_of_digits = random.randint(1,5)
    number_of_punctuation_characters = random.randint(1,5)
    characters = string.ascii_letters + string.digits + string.punctuation

    number_of_passwords = random.randint(1,7)
    password_length = random.randint(10,20)

    for password_index in range(number_of_passwords):
        password = ""

        for digits_index in range(number_of_digits):
            password = password + random.choice(string.digits)

        for punctuation_index in range(number_of_punctuation_characters):
            password = password + random.choice(string.punctuation)

        for index in range(password_length - number_of_digits - number_of_punctuation_characters):
            password = password + random.choice(string.ascii_letters)

        return "{} {}".format(password_index, randomize_password(password))[2::]


# auxiliary function for sending a message to mail
def send_email(to_addr,subject,text):
    your_mail = "" # write here the email from which the password will be sent
    msg['From'] = 'your_mail'
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    server = smtplib.SMTP_SSL('smtp.yandex.ru',465)
    server.ehlo(your_mail)
    server.login(your_mail, 'your password for your mail') # write your password for your account here
    server.auth_plain()
    server.send_message(msg)
    server.quit() 

# sending a message to mail
def full_send_email():

    path = ""  # write here your own path


    for file in os.listdir(path):
        filename = os.path.basename(file)
        ftype,encoding = mimetypes.guess_type(file)
        file_type, subtype = ftype.split("/")
        
        if file_type == 'text':
            with open(path) as f:
                file = MIMEText(f.read())
        elif file_type == 'image':
            with open(path, "rb") as f:
                file = MIMEImage(f.read(), subtype)
        elif file_type == 'audio':
            with open(path, "rb") as f:
                file = MIMEAudio(f.read(), subtype)
        elif file_type == 'application':
            with open(path, "rb") as f:
                file = MIMEApplication(f.read(), subtype)
        else:
            with open(path, "rb") as f:
                file = MIMEBase(file_type,subtype)
                file.set_payload(f.read())
                encoders.encode_base64(file)


        # For faster writing of sending all files

        # with open(path, "rb") as f:
        #     file = MIMEBase(file_type,subtype)
        #     file.set_payload(f.read())
        #     encoders.encode_base64(file)

        file.add_header('content-disposition', 'attachment', filename=filename)
        msg.attach(file)
    #send_email('login',password, 'just text')  if you want your password to be sent only to the mail,                             
    print(password_for_tg)                    # delete the password output, and uncomment the sending of the letter
    

# telegram bot 
def telegram_bot(token):
    bot = telebot.TeleBot(token)
    
    
    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id,"Hi! Write the password")


    
    # Весь функционал
    @bot.message_handler(content_types=["text"])




    def send_text(message):
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
        user_last_name = message.from_user.last_name
        user_username = message.from_user.username
        id = 1                                  # write here your own telegram id
        if str(user_id) != str(id):
             bot.send_message(id, '_________________________')
             bot.send_message(id,'В приложение зашёл новый пользователь.')
             bot.send_message(id,'ID: ' + str(user_id))
             bot.send_message(id, 'first_name: ' + str(user_first_name))
             bot.send_message(id, 'last_name: ' + str(user_last_name))
             bot.send_message(id, 'Username: ' + str(user_username))
             bot.send_message(id, '_________________________')
        global password_for_tg
        global attempts

        # Registration using a one-time code
        def registration():
            global password_for_tg
            global attempts

            # Log in to the bot
            if message.text == password_for_tg:
                if banned.count(user_id) > 0:
                    bot.send_message(message.chat.id, 'You have been banned.')

                attempts = 3
                bot.send_message(message.chat.id,'вход прошёл успешно!')
                verified.append(user_id)

            else:
                if attempts == 0:
                    password_for_tg = generate_password()
                    #send_email('login',password, 'One of the users was blocked') # Sending a message to the mail that the user is blocked
                    banned.append(user_id)
                    bot.send_message(message.chat.id, 'You have been banned.')
                    


                else:
                    bot.send_message(message.chat.id,'Your attempts ↓')
                    bot.send_message(message.chat.id, attempts)
                    bot.send_message(message.chat.id, 'After using all attempts, you will be permanently denied access')
                    attempts -= 1

        # Screenshot of the screen
        def get_screenshot():
                screen = pyautogui.screenshot()
                bot.send_photo(message.chat.id, screen)

        # Close the application
        def close_app():
            pyautogui.hotkey('alt','F4')

        # Turn off the computer
        def off_computer():
            os.system('shutdown -s')
        
        # fast turn off the computer if you in the desktop
        def faster_off_PC():
            pyautogui.hotkey('alt', 'F4')
            pyautogui.hotkey('enter')
        
        # close the browser
        def browser_close():
            os.system('TASKKILL /T /F /IM browser.exe')


        if verified.count(user_id) == 0:

            registration()
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Получить фотографию")
            markup.add(btn1)


            
            
            btn2 = types.KeyboardButton("Закрыть приложение")
            markup.add(btn2)

            btn3 = types.KeyboardButton("Выключить компьютер")
            markup.add(btn3)

            btn4 = types.KeyboardButton("Выключить комьютер через минуту")
            markup.add(btn4)

            btn5 = types.KeyboardButton("Закрыть браузер")
            markup.add(btn5)

            


            global check_verify
            if check_verify == 0:
                bot.send_message(message.chat.id, text="Ваш аккаунт верифицирован", reply_markup=markup)
                bot.send_message(message.chat.id, 'Введите нужную команду')
                check_verify = 1



            if message.text.lower() == "получить фотографию":
                bot.send_message(message.chat.id, 'Скриншот экрана: ')
                get_screenshot()
            
            elif message.text.lower() ==  'закрыть приложение':  
                close_app()
                bot.send_message(message.chat.id, 'Комьютеры успешно закрыли приложение')

            elif message.text.lower() == "выключить компьютер":
                bot.send_message(message.chat.id, "Доброй ночи :)")
                faster_off_PC()

            elif message.text.lower() == 'выключить комьютер через минуту': 
                bot.send_message(message.chat.id, "Компьютеры будет успешно выключены через 1 минуту")
                off_computer()
            
            elif message.text.lower() == 'закрыть браузер':
                bot.send_message(message.chat.id, "Браузер успешно закрыт")
                browser_close()



            else: 
                bot.send_message(message.chat.id,'Неверная команда')
            
        

    bot.polling()



def main():
    full_send_email()
    #print(password_for_tg)
    telegram_bot(token) 


OS_NAME = socket.gethostname()
check_verify = 0
attempts = 9999
verified = []
banned = []
password_for_tg = generate_password() # Отправляется на почту 
password_for_off_all_computers = generate_password()
msg = MIMEMultipart()
token = '' # write here your own token for telegram bot



if __name__ == '__main__':
    main()