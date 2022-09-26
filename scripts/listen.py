import asyncio

import socketio

sio = socketio.AsyncClient()


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
    await sio.emit('get_nicklist', {'room': 'blah'})


@sio.event
async def connect():
    print("I'm connected!")


async def main():
    await sio.connect('http://localhost:11160/')
    await sio.emit('join_room', {'room_name': 'blah'})
    await sio.emit('set_nick', {'nick': 'dan'})
    await sio.wait()

asyncio.get_event_loop().run_until_complete(main())
