import asyncio
import json
import logging


ACCOUNT_HASH = 'e54a90d6-11d8-11eb-8c47-0242ac110002\n'
logger = logging.getLogger('sender')
logger.setLevel(logging.DEBUG)
for handler in logger.handlers:
    logger.removeHandler(handler)

console = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
console.setFormatter(formatter)
logger.addHandler(console)


async def send_message():
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    logger.debug(repr(ACCOUNT_HASH))
    writer.write(ACCOUNT_HASH.encode())
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    user_features = json.loads(server_response)
    if not user_features:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    message = 'SPAAAAAM\n'
    writer.write('SPAAAAAM\n'.encode())
    writer.write(b'\n')
    logger.debug(repr(message))
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    writer.close()


def main():
    asyncio.run(send_message())


if __name__ == '__main__':
    main()
