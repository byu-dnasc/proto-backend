import pytest
import time

from globus.index import Index

_test_index_id = 'c051154f-b44a-4771-a5ba-87ca4888852c'

@pytest.fixture(scope='session')
def index_f():
    return Index(index_id=_test_index_id)

@pytest.fixture()
def load_index_f(index_f, movies_f):
    index_f.blocking_ingest(movies_f)

@pytest.fixture(autouse=True)
def wipe_index_f(index_f):
    yield
    r = index_f.SEARCH_CLIENT.delete_by_query(_test_index_id, {'q':'*'})
    task_id = r['task_id']
    timeout = time.time() + 10
    while True:
        time.sleep(0.5)
        task = index_f.SEARCH_CLIENT.get_task(task_id)
        if task['state'] == 'SUCCESS':
            print(task)
            break
        elif task['state'] == 'FAILED':
            raise Exception('Failed to wipe index: ' + task['message'])
        if time.time() > timeout:
            raise Exception('Wipe index fixture: Timeout waiting for task to complete')
    time.sleep(1) # server refresh interval

