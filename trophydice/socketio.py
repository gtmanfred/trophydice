from .utils.socket import SocketManager


sm = SocketManager(mount_location='/')


@sm.on('join_room')
async def handle_join_room(sid, data):
    room_name = data.get('room_name')
    sm.enter_room(sid, room_name)
    await sm.emit('joined', {'channel': f'{room_name}'}, to=sid)


@sm.on('set_nick')
async def set_sid_session_nick(sid, data):
    await sm.save_session(sid, data)


@sm.on('get_nicklist')
async def handle_get_nicklist(sid, data):
    sockets = sm.get_participants(namespace='/', room=data['room'])
    nicks = set()
    for socket in sockets:
        for sid in socket:
            try:
                session = await sm.get_session(sid=sid)
            except KeyError:
                continue
            if 'nick' in session:
                nicks.add(session['nick'])
    await sm.emit('nicklist', data={'nicks': sorted(nicks)}, to=sid)
