import asyncio
from datetime import datetime

import aiofiles


HOST = 'minechat.dvmn.org'
PORT = 5000


async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    try:
        while True:
            received_data = await reader.read(1000)
            async with aiofiles.open('chat_history.txt', 'a') as history_file:
                message = received_data.decode()
                formatted_datetime = datetime.now().strftime('%d.%m.%y %H:%M')
                log_note = f'{formatted_datetime} {message}'
                await history_file.write(log_note)
    except asyncio.CancelledError:
        raise
    finally:
        writer.close()


if __name__ == '__main__':
    asyncio.run(main())
