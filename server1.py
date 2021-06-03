import socket
import os
import sys
from datetime import datetime
from threading import Thread

port = 25

# создаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = ("0.0.0.0", port)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
def clientHandler(connection, count):
    sender_name = ""
    sender_mail = ""
    address_name = ""
    info = ""
    text = ""
    mess = "Welcome to the SMTP server! \n"
    connection.send(mess.encode())
    # Принимаем данные порциями и ретранслируем их
    try:
        while True:
            message = connection.recv(512).decode()

            if message != "" and message != "\n":
                print(f'Получено: {message}')

            if message.startswith("QUIT"):
                mess = "221 Bye! \n"
                connection.send(mess.encode())
                connection.close()
                break

            elif message.lower() == "helo" or message.lower() == "mail from" or message.lower() == "rcpt to":
                mess = "Please enter info"
                connection.send(mess.encode())

            elif message.lower().startswith("helo"):
                sender_name = message[4:]  # обрезать
                mess = "250 OK \n"

            elif message.startswith("MAIL FROM"):
                sender_mail = message[10:]
                mess = "250 OK \n"

            elif message.startswith("RCPT TO"):
                address_name = message[8:]
                mess = "250 OK \n"

            elif message.startswith("DATA"):
                info = message[4:]
                mess = "354 Send message content"
                connection.send(mess.encode())
                data = connection.recv(4096)
                text = data.decode()
                mess = "250 OK \n"
                storeLetter(sender_mail, sender_name, address_name, info, text, count)
                count += 1

            else:
                mess = "Invalid data \n"
            connection.send(mess.encode())

    except Exception as exp:
        print(exp)
        if sender_mail != "" and sender_name != "" and address_name != "" and text != "":
            storeLetter(sender_mail, sender_name, address_name, info, text, count)

    finally:
        connection.close()


def storeLetter(sender_mail, sender_name, address_name, info, text, count):
    letter = ""
    letter += "From: {} \n".format(sender_mail)
    letter += "Name: {} \n".format(sender_name)
    letter += "To: {} \n".format(address_name)
    letter += "Date: {} \n".format(datetime.today().strftime('%Y-%m-%d'))
    if info:
        letter = letter + info + "\n"
    letter += text

    path = os.curdir
    if not os.path.exists("Mail"):
        os.mkdir(path + "/Mail")
    os.chdir("Mail")
    name = "letter{}.txt".format(count)
    with open(name, "w") as file:
        file.write(letter)


sock.listen(5)
while True:
    try:
        # ждем соединения
        print('Waiting for requests...')
        count = 0
        connection, client_address = sock.accept()
        print('Connected to:', client_address)
        Thread(target=clientHandler(connection, count)).start()
    finally:
        # Очищаем соединение
        sock.close()
