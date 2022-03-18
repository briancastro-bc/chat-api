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
            sid,
            {
                'sid': sid,
                'operating_system': environ['HTTP_SEC_CH_UA_PLATFORM'],
            }
        )
        async with self.session(sid) as session:
            await self.emit(
                'connected',
                {
                    'message': 'New user connected from {0}'.format(session['operating_system'])
                }
            )
    
    async def on_create_room(
        self,
        sid: str,
    ):
        room: str = ChatNamespaceService.generate_code()
        if room in self.rooms:
            return await self.emit(
                'room_exists',
                {
                    "message": "The chat rooms exists",
                    "system_message": True
                }
            )
        self.rooms.append(room)
        await self.save_session(
            sid,
            {
                'user_room': room
            }
        )
        await self.emit(
            'room_created',
            {
                'message': 'New room created',
                'room': room
            }
        )
        await self.on_join_room(
            sid=sid,
            data={
                'room': room
            }
        )

    async def on_join_room(
        self,
        sid: str,
        data: dict[str, Any]
    ):
        if not data['room'] in self.rooms:
            return await self.emit(
                'room_not_found',
                {
                    'message': "The chat room doesn't exists",
                    'system_message': True
                }
            )
        self.enter_room(sid=sid, room=data['room'])
        await self.emit(
            'joined',
            {
                'message': 'New user joined into room #{0}'.format(data['room']),
                'system_message': True
            }
        )
        await self.send(
            {
                'message': 'User joined #{0} in the rom'.format(sid),
                'system_message': True
            },
            room=data['room']
        )
    
    async def on_message(
        self,
        sid: str,
        data: dict[str, Any]
    ):
        async with self.session(sid) as session:
            you = sid if session['sid'] == sid else None
            await self.send(
                {
                    'message': data['message'],
                    'user': data['user']
                },
                room=data['room']
            )

    async def on_leave_room(
        self,
        sid: str,
        data: dict[str, Any]
    ):
        self.leave_room(sid=sid, room=data['room'])
        await self.emit(
            'left',
            {
                'message': 'User left',
                'system_message': True
            }
        )
        await self.send(
            {
                'message': 'User #{0} left from the room'.format(sid),
                'system_message': True
            },
            room=data['room']
        )

    async def on_destroy_room(
        self,
        sid: str,
        data: dict[str, Any]
    ):
        if not data['room'] in self.rooms:
            return await self.emit(
                'room_not_found',
                {
                    'message': "The chat room doesn't exists",
                    'system_message': True
                }
            )
        await self.close_room(room=data['room'])
        self.rooms.remove(data['room'])
        await self.save_session(
            sid,
            {
                'user_room': ''
            }
        )
        await self.emit(
            'room_destroyed',
            {
                'message': 'The room #{0} was destroyed'.format(data['room']),
                'system_message': True
            }
        )

    async def on_disconnect(
        self,
        sid: str
    ):
        print('User disconnected #{1}'.format(sid))
        async with self.session(sid) as session:
            await self.emit(
                'disconnected',
                {
                    'message': 'User disconnected from {0}'.format(session['operating_system'])
                }
            )
            del session