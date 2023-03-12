from unittest.mock import MagicMock

import pytest

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService
from setup_db import db

@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    dir_1 = Director(id=1, name = 'Ivan')
    dir_2 = Director(id=2, name = 'Petr')
    dir_3 = Director(id=3, name = "Sidr")

    all_dir = [dir_1, dir_2, dir_3]

    director_dao.get_one = MagicMock(return_value = dir_1)
    director_dao.get_all = MagicMock(return_value = all_dir)
    director_dao.create = MagicMock(return_value = Director(id=3, name = 'Fedor'))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock(return_value = Director(id=2, name='Oleg'))

    return director_dao

class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) == 3
        assert len(directors) > 0

    def test_create(self):
        dir_data = {'name': 'Fedor'}
        director = self.director_service.create(dir_data)
        assert director.name == dir_data['name']

    def test_delete(self):
        director = self.director_service.delete(1)
        assert director is None

    def test_update(self):
        dir_data = {'id': 2, 'name': 'Oleg'}
        director = self.director_service.update(dir_data)
        assert director != None
        assert director.id == 2






