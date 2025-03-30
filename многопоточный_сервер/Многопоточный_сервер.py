import socket
import logging
import argparse

# Настройка логирования
logging.basicConfig(filename='server.log', level=logging.INFO)


def start_server(host='127.0.0.1', port=65432):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            s.bind((host, port))
            break
        except socket.error:
            port += 1
            print(f"Порт {port - 1} занят. Использую порт {port}")

    logging.info(f"Запуск сервера на {host}:{port}")
    print(f"Сервер запущен на {host}:{port}")
    s.listen()
    logging.info(f"Начало прослушивания порта {port}")

    while True:
        conn, addr = s.accept()
        logging.info(f"Подключение клиента {addr}")
        print(f"Клиент подключился: {addr}")

        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                logging.info(f"Прием данных от клиента: {data}")
                print(f"Прием данных от клиента: {data}")
                conn.sendall(data)
                logging.info(f"Отправка данных клиенту: {data}")
                print(f"Отправка данных клиенту: {data}")

            logging.info(f"Отключение клиента {addr}")
            print(f"Клиент отключился: {addr}")

        logging.info(f"Сервер продолжает слушать порт {port}")


def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Соединение с сервером {host}:{port}")
        s.connect((host, port))

        while True:
            message = input("Введите сообщение (или 'exit' для выхода): ")
            if message.lower() == 'exit':
                break
            s.sendall(message.encode())
            print(f"Отправка данных серверу: {message}")
            data = s.recv(1024)
            print(f"Прием данных от сервера: {data}")

        print(f"Разрыв соединения с сервером {host}:{port}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TCP Client/Server')
    parser.add_argument('--mode', choices=['server', 'client'], default='server')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=65432)
    args = parser.parse_args()

    if args.mode == 'server':
        start_server(args.host, args.port)
    elif args.mode == 'client':
        host = input("Введите имя хоста (по умолчанию: {}): ".format(args.host)) or args.host
        port = int(input("Введите номер порта (по умолчанию: {}): ".format(args.port)) or args.port)
        start_client(host, port)