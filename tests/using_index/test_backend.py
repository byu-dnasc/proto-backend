import pytest
import copy
from datetime import datetime, timedelta

import tests.conftest as conftest
import smrtlink.movies
from backend.backend import Backend

class TestBackend(Backend):
    def __init__(self, index_id=None):
        super().__init__(index_id=index_id)
        self.test_parameters = {}

    def set_test_parameters(self, **kwargs):
        self.test_parameters = kwargs
        return self

    def get_new_datasets(self):
        new_datasets = self.test_parameters['new_datasets']
        latest_movie_update = self.test_parameters['latest_movie_update']
        return new_datasets

def datetime_to_timestamp(timestamp: datetime):
    '''
    Given that:
    - SMRT Link timestamps are in milliseconds.
    - No positive evidence that Globus accepts microseconds.
    Therefore, use milliseconds throughout the project.
    Time zone is always UTC (append 'Z' for clarity)
    '''
    milliseconds = timestamp.microsecond // 1000
    timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
    timestamp_str += '.{:03d}'.format(milliseconds) + 'Z'
    return timestamp_str

def timestamp_to_datetime(timestamp: str):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

@pytest.fixture(scope='function')
def backend_f(index_f):
    return TestBackend(index_id=index_f.index_id)

@pytest.fixture(params=conftest.movie_ids)
def simulate_update_f(request, datasets_by_movie_id_f):
    movie_id = request.param
    datasets = datasets_by_movie_id_f[movie_id]
    datasets.sort(key=lambda ds: ds.created_at)
    all_datasets_but_latest = datasets[:-1]
    new_dataset = datasets[-1]
    movie = smrtlink.movies.get_new_movies(all_datasets_but_latest)[0]
    return movie, new_dataset

def test_update_index(index_f, backend_f, simulate_update_f):
    '''Simulate the circumstances under which the index would need updating.'''
    # get a movie and a latest dataset that belongs to it
    # but which has not yet been added
    movie_pre_update, new_dataset = simulate_update_f
    # verify that the movie is out of date
    updated_movie = smrtlink.movies.update_movies([copy.deepcopy(movie_pre_update)], [new_dataset])[0]
    assert movie_pre_update != updated_movie 
    # put the movie in the index
    index_f.blocking_ingest([movie_pre_update])
    # set the latest movie update to be one second before the 
    # new dataset so that the backend will recognize the dataset 
    # as new
    datetime = timestamp_to_datetime(new_dataset.created_at)
    datetime_one_second_ago = datetime - timedelta(seconds=1)
    out_of_date = datetime_to_timestamp(datetime_one_second_ago)
    assert out_of_date < new_dataset.created_at
    # configure the backend to with these artificial parameters
    # to simulate the circumstances under which an update would
    # be necessary
    backend_f.set_test_parameters(
        new_datasets=[new_dataset], 
        latest_movie_update=out_of_date
    )
    # see if the backend will bring the movie in index up to date
    backend_f.update_index()
    # get the movie from the index
    movie_post_update = index_f.get_movies(ids=[movie_pre_update.id])[0]
    # check that the movie has been updated
    assert movie_post_update == updated_movie