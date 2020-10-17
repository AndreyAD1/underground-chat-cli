import asyncio


HOST = 'minechat.dvmn.org'
PORT = 5000


async def tcp_client():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    try:
        while True:
            received_data = await reader.read(1000)
            print(received_data.decode().rstrip('\n'))
    except asyncio.CancelledError:
        raise
    finally:
        writer.close()


def main():
    asyncio.run(tcp_client())


if __name__ == '__main__':
    main()
