import pytest

import tests.read_test_data
import smrtlink.movies

_movies = tests.read_test_data.get_movies()
movie_ids = list(_movies.keys())

@pytest.fixture(scope='session')
def datasets_by_movie_id_f():
    return tests.read_test_data.get_datasets_by_movie_id()

@pytest.fixture(scope='session')
def movies_by_id_f():
    return _movies

@pytest.fixture(scope='session')
def movie_ids_f(movies_by_id_f):
    return list(movies_by_id_f.keys())

@pytest.fixture(scope='session')
def movies_f(movies_by_id_f):
    return [smrtlink.movies.MovieJson(movie_json) for movie_json in movies_by_id_f.values()]


@pytest.fixture(scope='session')
def jobs_json_f():
    return tests.read_test_data.get_jobs_json()

@pytest.fixture(scope='session')
def senarios_f():
    return tests.read_test_data.get_senarios()

