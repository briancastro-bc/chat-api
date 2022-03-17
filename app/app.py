from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

__all__ = ['create_application']

"""
    :function create_application - Define la configuracion de la aplicacion e instancia FASTAPI.
    :returns - Instancia de FastAPI
"""
def create_application() -> FastAPI:
    _app: FastAPI = FastAPI(
        debug=True,
        title='Chat API',
        description='Aplicacion de chat usando socket io como base',
        version='0.1.0'
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True,
        expose_headers=['']
    )

    return _app