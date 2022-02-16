import asyncio

import socketio

sio = socketio.AsyncClient()


@sio.event
async def message(data):
    print('I received a message!')


@sio.event
async def joined(data):
    print('joined', data)


@sio.on('v1/contest')
@sio.on('v1/risk')
async def rolls(data):
    print('rolled', data)


@sio.event
async def connect():
    print("I'm connected!")


async def main():
    await sio.connect('http://localhost:8000/')
    await sio.emit('join_room', {'room_name': 'test'})
    await sio.wait()

asyncio.get_event_loop().run_until_complete(main())
