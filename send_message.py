import asyncio


ACCOUNT_HASH = 'e54a90d6-11d8-11eb-8c47-0242ac110002\n'


async def send_message():
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)
    server_response = await reader.readline()
    print('Server response', server_response.decode())
    print(f'Send message: {ACCOUNT_HASH}')
    writer.write(ACCOUNT_HASH.encode())
    server_response = await reader.readline()
    print(f'Server response: {server_response.decode()}')
    server_response = await reader.readline()
    print(f'Server response: {server_response.decode()}')
    writer.write('SPAAAAAM\n'.encode())
    writer.write(b'\n')
    server_response = await reader.readline()
    print(f'Server response: {server_response.decode()}')
    writer.close()


def main():
    asyncio.run(send_message())


if __name__ == '__main__':
    main()
