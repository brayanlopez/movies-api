from fastapi import APIRouter

from fastapi import Path, Query, Depends
from fastapi.responses import  JSONResponse
from fastapi.enconders import jsonable_encoder
from typing import List

from schemas.Movie import Movie

from middlewares.jwt_bearer import JWTBearer

from config.database import Session
from models.Movie import Movie as MovieModel


movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.Query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.Query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"message":"Content not found"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=45)) -> List[Movie]:
    db = Session()
    result = db.Query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "movie created succesfully"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict)
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


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.Query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={"message":"Content not found"}, status_code=404)
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "movie deleted succesfully"}, status_code=200)

