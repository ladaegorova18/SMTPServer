import socket
import os
import sys
from datetime import datetime

port = 25

# создаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = ("localhost", port)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen(1)

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

while True:
    # ждем соединения
    print('Waiting for requests...')
    count = 0
    connection, client_address = sock.accept()
    try:
        print('Connected to:', client_address)
        sender_name = ""
        sender_mail = ""
        address_name = ""
        info = ""
        text = ""
        mess = "Welcome to the SMTP server!"
        connection.send(mess.encode())
        # Принимаем данные порциями и ретранслируем их
        while True:
            message = connection.recv(512).decode()
            print(f'Получено: {message}')

            if message.startswith("QUIT"):
                mess = "221 Bye!"
                connection.send(mess.encode())
                break

            elif message.startswith("HELO"):
                sender_name = message[4:] #обрезать
                mess = "250 OK"
                connection.send(mess.encode())

            elif message.startswith("MAIL FROM"):
                sender_mail = message[10:]
                mess = "250 OK"
                connection.send(mess.encode())

            elif message.startswith("RCPT TO"):
                address_name = message[8:]
                mess = "250 OK"
                connection.send(mess.encode())

            elif message.startswith("DATA"):
                info = message[4:]
                mess = "354 Send message content"
                connection.send(mess.encode())
                data = connection.recv(4096)
                text = data.decode()
                mess = "250 OK"
                connection.send(mess.encode())
                storeLetter(sender_mail, sender_name, address_name, info, text, count)
                count += 1

            else:
                print('No data from:', client_address)

    finally:
        # Очищаем соединение
        connection.close()