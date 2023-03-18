import socket
import sys
import os
import os.path
import errno
import time


def receive_log():
        log = conn.recv(1024).decode('UTF-8')
        passw = conn.recv(1024).decode('UTF-8')
        if log[0:4] == 'reg-':
            reg(log, passw)
        else:
            os.chdir('..')
            db = open('db.txt', 'r').readlines()
            for i in range(0, len(db)):
                db[i] = db[i].rstrip('\n').split('-')
            os.chdir('polucheno')
            flag = 0
            for i in range(0, len(db)):
                if log == db[i][0]:
                    count = i
                    flag = 1
                    break
                else:
                    flag = 0
            if flag == 1 and passw == db[i][1]:
                f = 'passed'
            elif flag == 1 and passw != db[i][1]:
                f = 'incpass'
            elif flag == 0:
                f = 'inclog'
            conn.send((bytes(f, encoding='UTF-8')))

def reg(log, passw):
    global conn
    os.chdir('..')
    f = open('db.txt', 'r+')
    data = f.read()
    f.write(log[4:] + '-' + passw + '\n')
    f.close()
    os.chdir('polucheno')

def redoconn():
    global conn, sock
    conn.close()
    sock.listen(15)
    conn, addr = sock.accept()

def answer():
    a = []
    if os.listdir() != a:
        for i in range(0, len(os.listdir())):
            a.append(os.listdir()[i][0:-4])
        print('Нашлись новые ответы на ваши запросы!')
        name = input('Список новых ответов: ' + str(a) + '\nВведите номер запроса, ответ которого вы хотите просмотреть: ')
        name = str(name)+'.txt'
        f = open(name,'r+')
        qu = f.readlines()
        print(qu[2])
        c = input('Ответ: ')
        f.write('\n'+c)
        f.close()
        conn.send((bytes(name, encoding='UTF-8')))
        f1 = open(name, "rb")
        # читаем строку
        l = f1.read(1024)
        while (l):
            # отправляем строку на сервер
            conn.send(l)
            l = f1.read(1024)
        f1.close()

def receive_file():
        name_f = (conn.recv(1024)).decode('UTF-8')
        f = open(name_f, 'wb')
        while True:
            # получаем байтовые строки
            l = conn.recv(1024)
            # пишем байтовые строки в файл на сервере
            f.write(l)
            if not l:
                break
        f.close()
        a = input('Получен новый запрос, желаете ответить? Введите "Да" или "Нет". ')
        if a.lower() == 'да':
            answer()
        elif a.lower() == 'нет':
            print('Не отлынивай от работы')
        else:
            print('Вы ввели не то, что указано в инструкции!')


try:
    os.mkdir('polucheno')
except OSError as e:
    if e.errno == errno.EEXIST:
        pass
    else:
        raise
os.chdir('polucheno')


# создаём сокет и связываем его с IP-адресом и портом
sock = socket.socket()
ip = "26.97.2.211"
port = 9997
sock.bind((ip, port))
# сервер ожидает передачи информации
sock.listen(15)

while True:
    # начинаем принимать соединения
    conn, addr = sock.accept()
    flag = 0
    # выводим информацию о подключении
    print('Подключился пользователь')
    f = (conn.recv(1024)).decode('UTF-8')
    print(f)
    if f == 'log' or f == 'reg':
        receive_log()
    elif f == 'запрос':
        receive_file()
