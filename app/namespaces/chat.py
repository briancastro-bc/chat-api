from typing import Any

from app.common.services import ChatNamespaceService

import socketio

class ChatNamespace(socketio.AsyncNamespace):

    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.rooms: list[Any] = []
    
    async def on_connect(
        self,
        sid: str,
        environ: Any,
        auth: Any
    ):
        print(environ)
        print(auth)
        print('New user connected #{0}'.format(sid))
        await self.save_session(
            #sid,
            {
                'operating_system': environ['HTTP']
            }
        )
    
    async def on_create_room(
        self,
        sid: str,
        data: Any
    ):
        if data['room'] in self.rooms:
            return await self.emit(
                'room_exists',
                {
                    "message": "The chat rooms exists",
                    "system_message": True
                }
            )
        room: str = ChatNamespaceService.generate_code()

        pass

    async def on_join_room(
        self,
        sid: str
    ):
        pass

    async def on_leave_room(
        self,
        sid: str
    ):
        pass

    async def on_destroy_room(
        self,
        sid: str
    ):
        pass

    async def on_disconnect(
        self,
        sid: str
    ):
        print('User disconnected #{1}'.format(sid))
        async with self.session(sid) as session:
            del session