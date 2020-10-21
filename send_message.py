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


async def register():
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
        user_token = None

    writer.close()
    await writer.wait_closed()
    return user_token


async def authorize(reader, writer, token):
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    logger.debug(repr(token))
    writer.write(f'{token}\n'.encode())
    await writer.drain()
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    user_features = json.loads(server_response)
    return user_features


async def submit_message(reader, writer, message_text):
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    logger.debug(repr(message_text))
    writer.write((message_text + '\n').encode())
    await writer.drain()
    writer.write(b'\n')
    await writer.drain()
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))


async def run_client():
    token = await register()
    if not token:
        error_message = 'Не удалось зарегистрировать нового пользователя.'
        logger.error(error_message)
        print(error_message)
        return

    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)
    user_features = await authorize(reader, writer, token)
    if not user_features:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return

    message = 'SPAAAAAM'
    await submit_message(reader, writer, message)
    writer.close()
    await writer.wait_closed()


def main():
    asyncio.run(run_client())


if __name__ == '__main__':
    main()
