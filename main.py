import asyncio
from datetime import datetime

import aiofiles
import configargparse


HOST = 'minechat.dvmn.org'
PORT = 5000


def get_input_arguments():
    pass


async def write_chat_history(host, port, output_file_path):
    reader, writer = await asyncio.open_connection(host, port)
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


async def main():
    input_arguments = get_input_arguments()
    chat_host, chat_port = input_arguments.host, input_arguments.port
    chat_history_file_path = input_arguments.history_file_path
    asyncio.run(main(chat_host, chat_port, chat_history_file_path))


if __name__ == '__main__':
    main()

