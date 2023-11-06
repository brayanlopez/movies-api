from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from routers.movie import movie_router
from routers.login import login_router
from utils.util import create_configuration_fastapi
from middlewares.error_handler import ErrorHandler

from config.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
create_configuration_fastapi(app, ErrorHandler, routers=[movie_router, login_router])


@app.get('/', tags=['home'], status_code=status.HTTP_200_OK)
def message():
    return HTMLResponse('<h1>Hello world</h1>')
