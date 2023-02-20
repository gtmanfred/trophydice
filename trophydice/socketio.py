from .utils.socket import SocketManager


sm = SocketManager(mount_location="/")


@sm.on("join_room")
async def handle_join_room(sid, data):
    room_name = data.get("room_name")
    sm.enter_room(sid, room_name)
    if sm.cache is not None:
        await sm.cache.delete(f"cache:{room_name}")
    await sm.emit("joined", {"channel": f"{room_name}"}, to=sid)


@sm.on("set_nick")
async def set_sid_session_nick(sid, data):
    await sm.save_session(sid, data)


@sm.on("get_nicklist")
async def handle_get_nicklist(sid, data):
    room = data.get("room", None)
    if room is None:
        return
    if sm.cache is not None and (nicks := await sm.cache.get(f"cache:{room}")):
        nicks = set(nicks.decode("utf-8").split(","))
    else:
        sockets = sm.get_participants(namespace="/", room=room)
        nicks = set()
        for socket in sockets:
            for socket_id in socket:
                try:
                    session = await sm.get_session(sid=socket_id)
                except KeyError:
                    continue
                if "nick" in session:
                    nicks.add(session["nick"])
        if sm.cache is not None:
            await sm.cache.set(f"cache:{room}", ",".join(nicks))
    await sm.emit("nicklist", data={"nicks": sorted(nicks)}, to=sid)
