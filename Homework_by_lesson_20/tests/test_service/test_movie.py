from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db

@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie_1 = Movie(id=1, title = 'fff', description = 'Комедия', trailer = 'trailer1', year = 2020, rating = 1.1, genre_id = 1, director_id = 1 )
    movie_2 = Movie(id=2, title = 'ddd', description = 'Драма', trailer = 'trailer2', year = 2021, rating = 5.1, genre_id = 2, director_id = 2 )
    movie_3 = Movie(id=3, title = 'eee', description = 'Thriller', trailer = 'trailer3', year = 2022, rating = 8.1,genre_id = 3, director_id = 3)

    all_movies = [movie_1, movie_2, movie_3]

    movie_dao.get_one = MagicMock(return_value = movie_1)
    movie_dao.get_all = MagicMock(return_value = all_movies)
    movie_dao.create = MagicMock(return_value = Movie(id=4, title = 'fff', description = 'Семейный', trailer = 'trailer4', year = 2019, rating = 6.1 ))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock(return_value = Movie(id=2, title = 'Супертриллер', description = 'Драма', trailer = 'trailer2', year = 2021, rating = 5.1 ))

    return movie_dao

class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None


    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) == 3
        assert len(movies) > 0

    def test_create(self):
        movie_data = {'title': 'fff'}
        movie = self.movie_service.create(movie_data)
        assert movie.title == movie_data['title']
        assert movie.title != 'aaa'
        assert movie.title == 'fff'

    def test_delete(self):
        movie = self.movie_service.delete(1)
        assert movie is None

    def test_update(self):
        movie_data = {'id': 2, 'title': 'Супертриллер'}
        movie = self.movie_service.update(movie_data)
        assert movie != None
        assert movie.id == 2
        assert movie.title == 'Супертриллер'