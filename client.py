import socket
import sys
from threading import Thread

port = 25

# СоздаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 84.252.138.83
# Подключаем сокет к порту, через который прослушивается сервер
server_address = ('localhost', port)
sock.connect(server_address)
print('Connected to {} port {}'.format(*server_address))
data = sock.recv(512)
answer = data.decode().replace('\n', '')
print(f'Received: {answer}')

def awaitAnswer():
    # Смотрим ответ
    data = sock.recv(512)
    answer = data.decode().replace('\n', '')
    print(f'Received: {answer}')


try:
    while True:
        # Отправка данных
        mess = input().split("\n")
        if mess != '' and mess != '\n':
            for line in mess:
                sock.sendall(line.encode())


        print(f'Sent: {mess}')

        Thread(target=awaitAnswer()).start()

finally:
    print('Closing...')
    sock.close()