import asyncio
import uuid
import sys
import webbrowser

import socketio

sio = socketio.AsyncClient()
ROOM = str(uuid.uuid4())


@sio.event
async def message(data):
    print('I received a message!')


@sio.event
async def joined(data):
    print('joined', data)

@sio.event
async def nicklist(data):
    print('nicklist', data)


@sio.on('v1/contest')
@sio.on('v1/risk')
async def rolls(data):
    print('rolled', data)
    await sio.emit('get_nicklist', {'room': ROOM})


@sio.event
async def connect():
    print("I'm connected!")


async def main(port):
    await sio.connect(f'http://localhost:{port}/socket.io/')
    await sio.emit('join_room', {'room_name': ROOM})
    await sio.emit('set_nick', {'nick': 'dan'})
    webbrowser.open_new(f'http://localhost:{port}/ui/{ROOM}')
    await sio.wait()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main(sys.argv[1]))
