import socket

port = 25

# СоздаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаем сокет к порту, через который прослушивается сервер
server_address = ('localhost', port)
print('Connected to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    while True:
        # Смотрим ответ
        data = sock.recv(512)
        print(f'Received: {data.decode()}')

        # Отправка данных
        mess = input()
        print(f'Sent: {mess}')
        sock.send(mess.encode())

finally:
    print('Closing...')
    sock.close()