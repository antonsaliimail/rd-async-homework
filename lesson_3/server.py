"""
У цьому домашньому завданні вам необхідно написати метеорологічний сервер та клієнт.

Сервер генеруватиме дані та надсилатиме їх усім клієнтам, які підключилися до нього. Клієнти читають дані й пишуть у консоль отриману інформацію.

Використати:

asyncio для мережевого коду
random для генерації даних
Формат здачі завдання:

Оформіть отриманий результат на GitHub і прикріпіть посилання у відповідне поле в LMS до цього уроку.
"""
import asyncio
import json
import random


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
):
    addr = writer.get_extra_info("peername")

    for i in range(10):
        data_to_send = {
            "temperature": random.randint(20, 100),
            "wind_speed": random.randint(20, 100),
            "humidity": random.randint(20, 100),
        }

        writer.write(json.dumps(data_to_send).encode())
        await writer.drain()

        print(f"Sent data to {addr}")

        await asyncio.sleep(1)

    exit_data = "exit"
    writer.write(exit_data.encode())
    await writer.drain()

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, "localhost", 8000)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
