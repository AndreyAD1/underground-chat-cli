import asyncio
import json
import logging
import re
import socket

import configargparse


logger = logging.getLogger('sender')
logger.setLevel(logging.DEBUG)
for handler in logger.handlers:
    logger.removeHandler(handler)

console = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
console.setFormatter(formatter)
logger.addHandler(console)


def get_input_arguments():
    argument_parser = configargparse.get_argument_parser()
    argument_parser.add(
        '--host',
        type=str,
        default='minechat.dvmn.org',
        env_var='CHAT_HOST',
        help='The chat address.'
    )
    argument_parser.add(
        '--port',
        type=int,
        default=5050,
        env_var='WRITING_PORT',
        help='The number of port the chat server listens.'
    )
    argument_parser.add(
        '--token',
        type=str,
        default='',
        env_var='USER_TOKEN',
        help='An existed user token the client should use to send a message.'
    )
    argument_parser.add(
        '--user_name',
        type=str,
        default='Script Bot',
        env_var='USER_NAME',
        help="""
        If user do not set the argument '--token', 
        the script will create a new user having this name.
        """
    )
    argument_parser.add(
        '--message',
        type=str,
        default='Hello everyone!',
        help='A message the client should send.'
    )
    input_arguments = argument_parser.parse_args()
    return input_arguments


async def register(host, port, user_name):
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except socket.gaierror:
        logger.error(f'Can not connect to {host}:{port}')
        return None
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))

    writer.write(b'\n')
    await writer.drain()
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))

    filtered_nick = re.sub('(\\\+n|\n|\\\+)', '', user_name)
    message_to_send = f'{filtered_nick}\n'
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
    decoded_response = server_response.decode()
    logger.debug(repr(decoded_response))
    try:
        user_features = json.loads(server_response)
    except json.JSONDecodeError:
        logger.error(
            f'Can not parse to JSON the server response: {decoded_response}.'
        )
        user_features = None
    return user_features


async def submit_message(reader, writer, message_text):
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))
    logger.debug(repr(message_text))
    filtered_message = re.sub('\n\n', '', message_text)
    writer.write((filtered_message + '\n').encode())
    await writer.drain()
    writer.write(b'\n')
    await writer.drain()
    server_response = await reader.readline()
    logger.debug(repr(server_response.decode()))


async def run_client(host, port, token, user_name, message):
    if not token:
        token = await register(host, port, user_name)
        if not token:
            error_message = 'Не удалось зарегистрировать нового пользователя.'
            logger.error(error_message)
            print(error_message)
            return

    try:
        reader, writer = await asyncio.open_connection(host, port)
    except socket.gaierror:
        error_message = f'Can not connect to {host}:{port}'
        logger.error(error_message)
        print(error_message)
        return

    user_features = await authorize(reader, writer, token)
    if not user_features:
        print('Не удалось получить свойства юзера.')
        print('Проверьте токен юзера и номер порта сервера.')
        return

    await submit_message(reader, writer, message)
    writer.close()
    await writer.wait_closed()


def main():
    input_arguments = get_input_arguments()
    user_token, user_name = input_arguments.token, input_arguments.user_name
    chat_host, chat_port = input_arguments.host, input_arguments.port
    message = input_arguments.message
    client = run_client(chat_host, chat_port, user_token, user_name, message)
    asyncio.run(client)


if __name__ == '__main__':
    main()
