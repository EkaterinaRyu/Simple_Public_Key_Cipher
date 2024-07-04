import socket
import pickle


def Reverse_XOR(A2):
    bit_str = ''   # Тут хранится двоичное представление полученного списка чисел
    s = ''
    for i in secret:  # Каждое полученное число преобразовываем в двоичный вид
        s = s + bin(i)[2:]
        while len(s) < 8:
            s = '0' + s
        bit_str = bit_str + s + ' '
        s = ''
    print(bit_str)  # Сообщение, преобразованное в двоичный вид
    print("XOR в другую сторону")
    secret_key = ''  # Создаем секретный ключ, которым и раскодируем сообщение
    k1 = ''
    for i in range(len(secret)):
        k1 = k1 + bin(A2 + i)[2:] + ' '
        while len(k1) <= 8:
            k1 = '0' + k1
        secret_key += k1
        k1 = ''
    print(secret_key)  # Ключ, преобразованный в двоичный вид

    str2 = ''  # Результат "обратного" побитового умножения
    c = ''
    for x, y in zip(bit_str.split(' '), secret_key.split(' ')):
        for i, j in zip(x, y):
            if i != j:
                c = c + '1'
            else:
                c = c + '0'
        str2 = str2 + c + ' '
        c = ''
    print('=')
    print(str2)  # Восстановлен двоичный код исходного сообщения
    print(' ')
    unsecret = ''  # Расшифрованное сообщение клиента
    for i in str2[:-2].split(' '):
        print(int(i, 2), end=' ')  # Номер символов по таблице ASCII
        unsecret = unsecret + chr(int(i, 2))
    print('\n')
    print('\033[34m'f"{unsecret}"'\033[39m')

    return unsecret


def create_server_key():
    msg = conn.recv(1024)  # получаем число от клиента
    msg = pickle.loads(msg)
    print(msg)

    a = 67

    A = 3 ** a % 17  # Некое число, которое отправим клиенту

    A2 = msg[0] ** a % 17  # Наш тайный ключ
    print("Наш ключ:", A2)
    conn.send(pickle.dumps((A)))  # Отправляем число клиенту

    return A2


def XOR(A2):
    global s
    print(s, '\n')
    bin_s = ''        # Преобразовываем наше сообщение в двоичное число
    for i in s:
        if i == ' ':
            bin_s = bin_s + '00' + bin(ord(i))[2:] + ' '
        else:
            bin_s = bin_s + '0' + bin(ord(i))[2:] + ' '
    print(bin_s)  # Двоичный вид нашего сообщения клиенту
    print('XOR')

    secret_key = ''  # Создаем ключ, которым закодируем сообщение
    k1 = ''
    for i in range(len(s)):
        k1 = k1 + bin(A2 + i)[2:] + ' '
        while len(k1) <= 8:
            k1 = '0' + k1
        secret_key += k1
        k1 = ''

    print(secret_key)     # Наш секретный ключ, которым закодируем сообщение

    str = ''    # Строка, в которую запишется результат побитового умножения
    c = ''
    for x, y in zip(bin_s.split(' '), secret_key.split(' ')):
        for i, j in zip(x, y):
            if i != j:
                c = c + '1'
            else:
                c = c + '0'
        str = str + c + ' '
        c = ''
    print('=')
    print(str)      # Результат побитового умножения

    str = str[:-2]      # То же самое что в str, только уже в виде чисел
    arr_final = []
    for i in str.split(' '):
        arr_final.append(int(i, 2))
    print(arr_final)
    return arr_final      # Возвращаем массив из чисел, который потом передадим


def create_client_key():
    p = 3
    q = 17
    a = 67

    A = p ** a % q
    conn.send(pickle.dumps((A, p, q)))     # Число клиента для создания ключа

    msg = conn.recv(1024)
    msg = pickle.loads(msg)
    print(msg)

    A2 = msg ** a % 17      # Наш ключ
    print("Наш ключ:", A2)
    return A2


HOST = '127.0.0.1'
PORT = 9095

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

while True:
    A2 = create_server_key()  # Создаем секретный ключ

    secret = conn.recv(1024)  # Считываем закодированный список чисел
    secret = pickle.loads(secret)
    print(secret)  # Выводим закодированный список

    Reverse_XOR(A2)  # Вызываем функцию расшифровки закодированного списка чисел

    # ----------------------------------Отправка сообщений от сервера клиенту---------------------------------------------------

    print('\033[32m"Введите сообщение:"\033[39m')
    s = input()  # Вводим сообщение с клавиатуры
    A2 = create_client_key()  # Создание секретного ключа
    arr_final = XOR(A2)  # Шифруем сообщение секретным ключом
    conn.send(pickle.dumps(arr_final))  # Отправляем зашифрованное сообщение

conn.close()

