from fastapi import FastAPI, Body, Path, Query, status, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.enconders import jsonable_encoder
from typing import List
from data.data import movies
from schemas.Movie import Movie
from schemas.User import User
from utils.util import create_configuration_fastapi
from jwt_manager import create_token, validate_token

from config.database import Session, engine, Base
from models.Movie import Movie as MovieModel

Base.metadata.create_all(bind=engine)

app = FastAPI()
create_configuration_fastapi(app)


class JWTBearer():
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com" or data["password"] != "admin":
            raise HTTPException(status_code=401, detail="invalid credentials")


@app.get('/', tags=['home'], status_code=status.HTTP_200_OK)
def message():
    return HTMLResponse('<h1>Hello world</h1>')


@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.Query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@app.get('/movies/{id}', tags=['movies'], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.Query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"message":"Content not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=45)) -> List[Movie]:
    db = Session()
    result = db.Query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "movie created succesfully"})


@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.Query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"message":"Content not found"}, status_code=404)
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(content={"message": "movie modified succesfully"})


@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.Query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"message":"Content not found"}, status_code=404)
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "movie deleted succesfully"}, status_code=200)


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token_bytes = create_token(user.model_dump())
        return JSONResponse(content=token_bytes, status_code=200)
