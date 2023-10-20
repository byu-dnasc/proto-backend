import pytest

import smrtlink.movies
import tests.conftest as conftest # hopefully not circular or otherwise problematic

@pytest.fixture(params=conftest.movie_ids)
def input_output_f(request, datasets_by_movie_id_f, movies_by_id_f):
    input_datasets = datasets_by_movie_id_f[request.param]
    output_movie = smrtlink.movies.MovieJson(movies_by_id_f[request.param])
    return input_datasets, output_movie

def test_get_new_movies(input_output_f):
    datasets, correct = input_output_f
    movie = smrtlink.movies.get_new_movies(datasets)[0]
    assert movie == correct