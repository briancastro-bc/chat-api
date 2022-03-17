from fastapi import FastAPI
from app.app import create_application
from app.io import create_io_server

import socketio

app: FastAPI = create_application()
sio: socketio.AsyncServer = create_io_server()
sio_app = socketio.ASGIApp(
    sio,
    app
)

@app.on_event('startup')
async def on_startup():
    print('Starting application')

@app.on_event('shutdown')
async def on_shutdown():
    print('Stop application')