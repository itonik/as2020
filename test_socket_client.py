import asyncio

async def echo_reader(reader, writer):
    while True:
        data = await reader.readline()
        msg = f'Got {data.decode()}'
        print(msg)
        writer.write(msg.encode())


async def delay_writer(writer: asyncio.StreamWriter):
    counter = 0
    while True:
        writer.write(f'ping {counter}...\n'.encode())
        counter += 1
        await asyncio.sleep(4)
        await writer.drain()


async def test_client(port=8001):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', port)

    asyncio.create_task(echo_reader(reader, writer))
    asyncio.create_task(delay_writer(writer))

if __name__ == '__main__':
    asyncio.run(test_client())
