from .utils.socket import SocketManager


sm = SocketManager(mount_location='/')


@sm.on('join_room')
async def handle_join_room(sid, data):
    room_name = data.get('room_name')
    sm.enter_room(sid, room_name)
    await sm.emit('joined', {'channel': f'{room_name}'}, to=sid)
