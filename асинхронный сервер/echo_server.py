import asyncio
import signal

clients = set()

async def handle_echo(reader, writer):
    clients.add(writer)
    try:
        while True:
            data = await reader.read(100)
            if not data:
                break  # Если данные не получены, клиент отключился
            message = data.decode()
            print(f"Получено сообщение: {message}")

            # Отправка сообщения всем клиентам
            for client in clients:
                client.write(data)
                await client.drain()
    finally:
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    print("Сервер запущен на 127.0.0.1:8888")

    async with server:
        await server.serve_forever()

def shutdown(signal, loop):
    print(f"Получен сигнал завершения: {signal.name}")
    for client in clients:
        client.close()
    loop.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown, sig, loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Сервер остановлен.")