import asyncio
from datetime import datetime

import aiofiles
import configargparse

from logger import logger
from open_connection import open_connection


def get_input_arguments():
    argument_parser = configargparse.get_argument_parser()
    argument_parser.add(
        '--host',
        type=str,
        default='minechat.dvmn.org',
        env_var='CHAT_HOST',
        help='An address of the chat host.'
    )
    argument_parser.add(
        '--port',
        type=int,
        default=5000,
        env_var='READING_PORT',
        help='A number of port which the chat server listens.'
    )
    argument_parser.add(
        '--history',
        type=str,
        default='chat_history.txt',
        env_var='HISTORY_FILEPATH',
        help='A file path where script should output result.'
    )
    input_arguments = argument_parser.parse_args()
    return input_arguments


async def write_chat_history(host, port, output_file_path):
    async with open_connection(host, port) as (reader, writer):
        while True:
            formatted_datetime = datetime.now().strftime('%d.%m.%y %H:%M')
            received_data = await reader.readline()
            message = received_data.decode()
            log_note = f'{formatted_datetime} {message}'
            try:
                async with aiofiles.open(output_file_path, 'a') as file:
                    await file.write(log_note)
            except FileNotFoundError:
                logger.error(f'Can not write to the file {output_file_path}')
                return


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
