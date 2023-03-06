from unittest.mock import MagicMock
import pytest

from dao.movie import MovieDAO
from dao.model.movie import Movie
from setup_db import db
from service.movie import MovieService

@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    alfa = Movie(id=1, title='alfa', description='description', trailer='trailer', year=1921, rating=2.0, genre_id=1, director_id=1,)
    grom = Movie(id=2, title='grom', description='description2', trailer='trailer2', year=1931, rating=3.1, genre_id=3, director_id=2,)

    movie_dao.get_one = MagicMock(return_value=alfa)
    movie_dao.get_all = MagicMock(return_value=[alfa, grom])
    movie_dao.create = MagicMock(return_value=Movie(id=3, title='titanic'))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao

class TestMovieService:

    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1
        assert movie.title == 'alfa'

    def test_get_all(self):
        movie = self.movie_service.get_all()
        assert len(movie) > 0

    def test_create(self):
        movie_d = {'id': 3,
                   'title': 'titanic'
        }
        movie = self.movie_service.create(movie_d)
        assert movie_d['title'] == movie.title

    def test_delete(self):
        movie = self.movie_service.delete(2)
        assert movie is None

    def test_update(self):
        movie_d = {
            'id': 2,
            'title': 'hero'
        }
        self.movie_service.update(movie_d)