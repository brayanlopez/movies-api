from fastapi import APIRouter

from fastapi import Path, Query, Depends
from fastapi.responses import  JSONResponse
from fastapi.enconders import jsonable_encoder
from typing import List

from schemas.Movie import Movie

from middlewares.jwt_bearer import JWTBearer

from config.database import Session
from models.Movie import Movie as MovieModel

from services.movie import MovieService

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:    
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"message":"Content not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=45)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "movie created succesfully"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"message":"Content not found"}, status_code=404)
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "movie modified succesfully"})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"message":"Content not found"}, status_code=404)
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "movie deleted succesfully"}, status_code=200)

