import socket
import pickle


def XOR(A2):
    print(s, '\n')
    bin_s = ''  # преобразовываем каждый символ в байт
    for i in s:
        if i == ' ':
            bin_s = bin_s + '00' + bin(ord(i))[2:] + ' '
        else:
            bin_s = bin_s + '0' + bin(ord(i))[2:] + ' '
    print(bin_s)  # Двоичный вид сообщения
    print('XOR')

    secret_key = ''  # Создаем ключ, которым закодируем сообщение
    k1 = ''  # каждый раз k1 хранит двоичное представление каждого символа, и каждый раз обнуляется
    for i in range(len(s)):
        k1 = k1 + bin(A2 + i)[2:] + ' '
        while len(k1) <= 8:
            k1 = '0' + k1
        secret_key += k1
        k1 = ''

    print(secret_key)  # Наш секретный ключ, которым закодируем сообщение
    # _____________________________________________

    result_str = ''  # Строка, в которую запишется результат побитового умножения
    c = ''
    # Проходим параллельно по исходной строке и строке-ключу
    for x, y in zip(bin_s.split(' '), secret_key.split(' ')):
        for i, j in zip(x, y):
            if i != j:
                c = c + '1'
            else:
                c = c + '0'
        result_str = result_str + c + ' '
        c = ''
    print('=')
    print(result_str)  # Результат побитового умножения
    result_str = result_str[:-2]
    arr_final = []  # То же самое что в str, только уже в виде чисел
    for i in result_str.split(' '):
        arr_final.append(int(i, 2))
    print(arr_final)
    return arr_final  # Возвращаем массив из чисел, который потом передадим


def create_client_key():
    p = 3
    q = 17
    a = 84
    A = p ** a % q
    sock.send(pickle.dumps((A, p, q)))

    msg = sock.recv(1024)    # Получаем число от сервера, чтобы создать ключ
    msg = pickle.loads(msg)
    print(msg)

    A2 = msg ** a % 17    # Наш ключ
    print("Наш ключ:", A2)
    return A2


def Reverse_XOR(A2):
    print(A2)
    str = ''
    s = ''
    for i in secret:    # Каждое полученное число преобразовываем в двоичный вид
        s = s + bin(i)[2:]
        while len(s) < 8:
            s = '0' + s
        str = str + s + ' '
        s = ''
    print(str)  # Сообщение, преобразованное в двоичный вид
    print("XOR в другую сторону")
    secret_key = ''
    k1 = ''
    for i in range(len(secret)):
        k1 = k1 + bin(4 + i)[2:] + ' '
        while len(k1) <= 8:
            k1 = '0' + k1
        secret_key += k1
        k1 = ''
    print(secret_key)  # Ключ, преобразованный в двоичный вид

    str2 = ''    # Строка, в которую запишется результат "обратного" побитового умножения
    c = ''
    for x, y in zip(str.split(' '), secret_key.split(' ')):
        for i, j in zip(x, y):
            if i != j:
                c = c + '1'
            else:
                c = c + '0'
        str2 = str2 + c + ' '
        c = ''
    print('=')
    print(str2)    # Восстановлен двоичный код исходного сообщения
    print(' ')
    unsecret = ''   # В эту переменную получим расшифрованное сообщение сервера
    for i in str2[:-2].split(' '):
        print(int(i, 2), end=' ')  # Номер символов по таблице ASCII
        unsecret = unsecret + chr(int(i, 2))
    print('\n')
    print('\033[34m'f"{unsecret}"'\033[39m')
    return unsecret


def create_server_key():
    global secret
    msg = sock.recv(1024)
    msg = pickle.loads(msg)
    print(msg)
    a = 84    # наше секретное число
    A = 3**a % 17
    sock.send(pickle.dumps((A)))

    A2 = msg[0]**a % 17
    print("Наш ключ:", A2)
    # with open("Закрытый ключ.txt", "a") as file:
    #     file.write(f'{A2}\n')
    secret = sock.recv(1024)
    secret=pickle.loads(secret)
    print(secret)
    return A2


HOST = '127.0.0.1'
PORT = 9095
sock = socket.socket()
sock.connect((HOST, PORT))

while True:
    print('\033[32m"Введите сообщение:"\033[39m')

    s = input()        # Вводим сообщение
    A2 = create_client_key()    # Создаем ключ
    arr_final = XOR(A2)        # Кодируем наше сообщение с помощью ключа
    sock.send(pickle.dumps(arr_final))    # Отсылаем наше сообщение

# ----------------------------------Получение сообщений от сервера---------------------------------------------------

    A2 = create_server_key()         # Создаем секретный ключ
    Reverse_XOR(A2)  # Вызываем функцию расшифровки сообщения


sock.close()

# ________________________________________________________________________