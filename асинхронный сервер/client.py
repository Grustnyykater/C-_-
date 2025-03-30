import asyncio

async def tcp_echo_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)

    while True:
        message = input("Введите сообщение (или 'exit' для выхода): ")
        if message.lower() == 'exit':
            break

        print(f"Отправка сообщения: {message}")
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        print(f"Получено сообщение: {data.decode()}")

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(tcp_echo_client('127.0.0.1', 8888))