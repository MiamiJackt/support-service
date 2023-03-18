import datetime
import socket
import sys
import os
import random
import time
from functools import lru_cache
import errno

@lru_cache(None)

def getip():
    global ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((ip, 9997))
    return (s.getsockname()[0])

def authenticate():
    global sock
    while True:
            a = input('Войдите в систему или зарегистрируйтесь\nЧтобы войти в систему - введите log\nЧтобы зарегистрироваться в системе - введите reg\n')
            if a.lower() == 'log':
                    connect()
                    sock.send((bytes(a.lower(), encoding='UTF-8')))
                    login()
                    break
            elif a.lower() == 'reg':
                    connect()
                    sock.send((bytes(a.lower(), encoding='UTF-8')))
                    register()
                    continue
            else:
                print('Вы ввели не то, что указано в инструкции')
                continue
            return login

def connect():
    global sock,ip,port
    sock = socket.socket()
    sock.connect((ip, port))

def reconnect():
    global sock,ip,port
    sock.close()
    sock = socket.socket()
    sock.connect((ip, port))

def register():
    global log,port,sock
    login = input('Введите логин: ')
    login = 'reg-'+login
    passw = input('Введите пароль: ')
    sock.send((bytes(login, encoding='UTF-8')))
    sock.send((bytes(passw, encoding='UTF-8')))
    reconnect()

def login():
        global log,ip,port,sock
        login1 = input('Введите логин: ')
        passw1 = input('Введите пароль: ')
        flag = False
        sock.send((bytes(login1, encoding='UTF-8')))
        sock.send((bytes(passw1, encoding='UTF-8')))
        f = (sock.recv(1024)).decode('UTF-8')
        if f == 'passed':
            print('Добро пожаловать в систему,',login1)
            log = login1
            pass
        elif f == 'incpass':
            print('Неверно введён пароль')
            quit()
        elif f == 'inclog':
            print('Неверно введён логин')
            quit()




def choose():
    global ip, port
    while True:
        a = input('Что вы хотите сделать?\n'
              'Чтобы создать новый запрос - напишите "запрос",\n'
              'Чтобы ждать новые файлы - напишите "ждать".\n')
        if a.lower() == 'запрос':
            reconnect()
            sock.send((bytes(a.lower(), encoding='UTF-8')))
            create()
        elif a.lower() == 'ждать':
            reconnect()
            receive_file()
            break
            continue
        else:
            print('Вы ввели не то, что указано в инструкции!')
            continue

def receive_file():
    while True:
        name_f = (sock.recv(1024)).decode('UTF-8')
        print(name_f)
        f = open(name_f, 'wb')
        while True:
            # получаем байтовые строки
            l = sock.recv(1024)
            # пишем байтовые строки в файл на сервере
            f.write(l)
            if not l:
                break
        f.close()
        a = input('Получен новый ответ, желаете посмотреть его? Введите "Да" или "Нет". ')
        if a.lower() == 'да':
            check()
        elif a.lower() == 'нет':
            print('Хорошо, на этом пока что всё.')
        else:
            print('Вы ввели не то, что указано в инструкции!')

def check():
    a = []
    if os.listdir() != a:
        for i in range(0,len(os.listdir())):
            a.append(os.listdir()[i][0:-4])
        print('Нашлись новые ответы на ваши запросы!')
        while True:
            b = input('Желаете просмотреть ответ и выставить ему статус?\nВведите "Да" или "Нет".\n')
            if b.lower() == 'да':
                status(a)
                break
            elif b.lower() == 'нет':
                print('Хорошо, тогда на этом пока что всё.')
                break
            else:
                print('Вы не ввели "Да" или "Нет".')
                continue
    else:
        print('Нет новых ответов на ваши запросы.')

def status(db):
    a = input('Список новых ответов: '+str(db)+'\nВведите номер запроса, ответ которого вы хотите просмотреть: ')
    print(db)
    f = open(a+'.txt','r+')
    qu = f.readlines()
    print(qu[2])
    while True:
        b = input('Вы удовлетворены ответом? Введите "Да" или "Нет" ')
        if b.lower() == 'да':
            f.write('\nПользователь удовлетворён ответом')
            f.close()
            print('Благодарим вас за использование новейшей разработки студентов СПБГМТУ!')
            break
        elif b.lower() == 'нет':
            f.write('\nПользователь неудовлетворён ответом')
            f.close()
            print('Благодарим вас за использование новейшей разработки студентов СПБГМТУ!')
            break
        else:
            print('Вы не ввели "Да" или "Нет".')
            continue

def create():
    global log,ip1, timenow, sock
    vopros = input('Введите вопрос: ')
    f_name = str(random.randint(1, 10000)) + '.txt'
    print(f_name)
    f = open(f_name, 'w')
    f.write(log + ', ' + timenow+'\n'+ip1+'\n')
    f.write(vopros)
    f.close()
    sock.send((bytes(f_name, encoding='UTF-8')))
    # открываем файл в режиме байтового чтения
    f = open(f_name, "rb")

    # читаем строку
    l = f.read(1024)

    while (l):
        # отправляем строку на сервер
        sock.send(l)
        l = f.read(1024)
    f.close()
    os.remove(f_name)
    sock.close()




ip = "26.97.2.211"
ip1 = getip()
port = 9997
f = True
try:
    os.mkdir('polucheno')
except OSError as e:
    if e.errno == errno.EEXIST:
        pass
    else:
        raise
os.chdir('polucheno')
timenow = datetime.datetime.now()
timenow = timenow.strftime('%d-%m-%Y %H:%M')
log = ''
authenticate()
choose()
