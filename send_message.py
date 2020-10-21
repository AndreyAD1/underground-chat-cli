import asyncio
import json
import logging


NICK_NAME = 'SCRIPT_BOT'
logger = logging.getLogger('sender')
logger.setLevel(logging.DEBUG)
for handler in logger.handlers:
    logger.removeHandler(handler)

console = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
console.setFormatter(formatter)
logger.addHandler(console)


async def sign_up():
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    writer.write(b'\n')
    await writer.drain()
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    message_to_send = f'{NICK_NAME}\n'
    logger.debug(repr(message_to_send))
    writer.write(message_to_send.encode())
    await writer.drain()
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    user_features = json.loads(server_response)
    try:
        user_token = user_features['account_hash']
    except (AttributeError, KeyError):
        error_message = 'Не удалось зарегистрировать нового пользователя.'
        logger.error(error_message)
        print(error_message)
        user_token = None

    writer.close()
    await writer.wait_closed()
    return user_token


async def sign_in(token):
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    logger.debug(repr(token))
    writer.write(f'{token}\n'.encode())
    await writer.drain()
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
    await writer.drain()
    writer.write(b'\n')
    await writer.drain()
    logger.debug(repr(message))
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    writer.close()
    await writer.wait_closed()


async def send_message():
    token = await sign_up()
    await sign_in(token)


def main():
    asyncio.run(send_message())


if __name__ == '__main__':
    main()
