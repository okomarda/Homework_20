from unittest.mock import MagicMock

import pytest

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService
from setup_db import db

@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    gen_1 = Genre(id=1, name = 'Комедия')
    gen_2 = Genre(id=2, name = 'Триллер')
    gen_3 = Genre(id=3, name = "Драма")

    all_gen = [gen_1, gen_2, gen_3]

    genre_dao.get_one = MagicMock(return_value = gen_1)
    genre_dao.get_all = MagicMock(return_value = all_gen)
    genre_dao.create = MagicMock(return_value = Genre(id=4, name = 'Семейный'))
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock(return_value = Genre(id=2, name='Супертриллер'))

    return genre_dao

class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id == 1

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) == 3
        assert len(genres) > 0

    def test_create(self):
        gen_data = {'name': 'Семейный'}
        genre = self.genre_service.create(gen_data)
        assert genre.name == gen_data['name']
        assert genre.name != 'Боевик'
        assert genre.name == 'Семейный'

    def test_delete(self):
        genre = self.genre_service.delete(1)
        assert genre is None

    def test_update(self):
        gen_data = {'id': 2, 'name': 'Супертриллер'}
        genre = self.genre_service.update(gen_data)
        assert genre != None
        assert genre.id == 2
        assert genre.name == 'Супертриллер'