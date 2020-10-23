import asyncio
from datetime import datetime
import socket

import aiofiles
import configargparse

from logger import logger


def get_input_arguments():
    argument_parser = configargparse.get_argument_parser()
    argument_parser.add(
        '--host',
        type=str,
        required=True,
        env_var='CHAT_HOST',
        help='An address of the chat host.'
    )
    argument_parser.add(
        '--port',
        type=int,
        required=True,
        env_var='READING_PORT',
        help='A number of port which the chat server listens.'
    )
    argument_parser.add(
        '--history',
        type=str,
        required=True,
        env_var='HISTORY_FILEPATH',
        help='A file path where script should output result.'
    )
    input_arguments = argument_parser.parse_args()
    return input_arguments


async def write_chat_history(host, port, output_file_path):
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except socket.gaierror:
        logger.error(f'Can not connect to {host}')
        return
    try:
        while True:
            received_data = await reader.read(1000)
            async with aiofiles.open(output_file_path, 'a') as history_file:
                message = received_data.decode()
                formatted_datetime = datetime.now().strftime('%d.%m.%y %H:%M')
                log_note = f'{formatted_datetime} {message}'
                await history_file.write(log_note)
    except asyncio.CancelledError:
        raise
    finally:
        writer.close()


def main():
    input_arguments = get_input_arguments()
    chat_host, chat_port = input_arguments.host, input_arguments.port
    chat_history_file_path = input_arguments.history
    main_coroutine = write_chat_history(
        chat_host,
        chat_port,
        chat_history_file_path
    )
    asyncio.run(main_coroutine)


if __name__ == '__main__':
    main()

