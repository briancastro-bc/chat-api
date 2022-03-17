from app import namespaces

import socketio

__all__ = ['io_server']

def create_io_server() -> socketio.AsyncServer:
    _io_server = socketio.AsyncServer(
        logger=True,
        always_connect=True,
        async_mode='asgi',
        ping_interval=30000,
        ping_timeout=100000,
        cookie='socket_session',
        cors_allowed_origins=['*'],
        cors_credentials=True
    )

    _io_server.register_namespace(
        namespaces.ChatNamespace(
            namespace='/chat'
        )
    )

    return _io_server