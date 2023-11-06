from schemas.Movie import Movie
from models.Movie import Movie as MovieModel

class MovieService():

  def __init__(self, db)-> None:
    self.db = db

  def create_movie(self, movie: Movie):
    new_movie = MovieModel(**movie.dict())
    self.db.add(new_movie)
    self.db.commit()
    return

  def get_movies(self):
    return self.db.query(MovieModel).all()
  
  def get_movie(self, id: int):
    return self.db.query(MovieModel).filter(MovieModel.id == id).first()
  
  def get_movie_by_category(self, category:str):
    return self.db.query(MovieModel).filter(MovieModel.category == category).all()

  def update_movie(self, id: int, movie: Movie):
    movie = self.db.Query(MovieModel).filter(MovieModel.id == id).first()
    if not movie:
        return 
    movie.title = movie.title
    movie.overview = movie.overview
    movie.year = movie.year
    movie.rating = movie.rating
    movie.category = movie.category
    self.db.commit()
    return 
  
  def delete_movie(self, id : int):
    result = self.get_movie(id)
    self.db.delete(result)
    self.db.commit()
    return 
