import globus_sdk
import json
import time
import re

from globus.auth import get_authorizer
from globus.const import Constants
import smrtlink.movies

def g_search_result_to_movies(g_search_result):
    g_meta_results = g_search_result['gmeta']
    movies = []
    for result in g_meta_results:
        dnascapp_entries = [e for e in result['entries'] if e['entry_id'] == 'dnascapp']
        if dnascapp_entries:
            movie_json = smrtlink.movies.MovieJson(dnascapp_entries[0]['content'])
            movies.append(movie_json)
        else:
            raise Exception('No entry found in gmeta result for dnascapp')
    return movies

def movies_to_g_meta_list(movies) -> dict:
    entries = [{
        'id': 'dnascapp',
        'subject': movie.id,
        'visible_to': Constants.VISIBLE_TO_URNS,
        'content': movie.to_dict()
    } 
    for movie in movies]
    g_meta_list = {
        "ingest_type": "GMetaList",
        "ingest_data": {
            'gmeta': entries
        }
    }
    return g_meta_list

class Index:
    _instance = None
    server_refresh_interval = 1 # delay in seconds between SUCCESS state of task and availability (of absence) of requested data across all servers

    # singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            index_id = kwargs.pop('index_id', None)
            cls._instance = super(Index, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize(index_id)
        return cls._instance

    def _initialize(self, index_id):
        SEARCH_SCOPE='urn:globus:auth:scope:search.api.globus.org:all'
        self.authorizer = get_authorizer(SEARCH_SCOPE)    
        self.SEARCH_CLIENT = globus_sdk.SearchClient(authorizer=self.authorizer)
        if index_id is None:
            self.index_id = '514074ce-90f1-4a1a-9feb-f74f7423735f'
        else:
            self.index_id = index_id

    def _wait_on_task(self, task_id):
        '''Wait for a task to complete'''
        timeout = time.time() + 10
        while True:
            time.sleep(0.5) # 5 requests per second is the rate limit, don't hog
            task = self.SEARCH_CLIENT.get_task(task_id)
            if task['state'] == 'SUCCESS':
                print(task)
                break
            elif task['state'] == 'FAILED':
                raise Exception('Task failed: ' + task['message'])
            if time.time() > timeout:
                raise Exception('Timeout waiting for task to complete')
    
    def ingest(self, g_meta_list):
        r = self.SEARCH_CLIENT.ingest(self.index_id, g_meta_list)
        try:
            self._wait_on_task(r['task_id'])
        except Exception as e:
            raise Exception('Failed to ingest: ' + str(e))
    
    def async_ingest(self, movies):
        '''Ingested data isn't guaranteed to be available immediately upon return.'''
        self.ingest(movies_to_g_meta_list(movies))
    
    def blocking_ingest(self, movies):
        self.ingest(movies_to_g_meta_list(movies))
        time.sleep(self.server_refresh_interval)

    def get_latest_movie_update(self):
        '''Get the string representation of the latest dataset timestamp from the index'''
        q = (globus_sdk.SearchQuery()
            .set_advanced(True)
            .set_query('*')
            .set_limit(1)
            .add_sort(field_name='updated_at', order='desc'))
        r = self.SEARCH_CLIENT.post_search(self.index_id, q)
        match = re.search(r'"updated_at"\s*:\s*"([^"]+)"', str(r))
        return match.group(1)
    
    def get_movies(self, ids=None):
        ''' Get a list of movies from the index by their dataset ids.'''
        by_id_query = (globus_sdk.SearchQuery()
                       .add_filter('id', ids, type='match_any'))
        all_query = globus_sdk.SearchQuery().set_query('*')
        if ids:
            query = by_id_query
        else:
            query = all_query
        r = self.SEARCH_CLIENT.post_search(self.index_id, query)
        movies = g_search_result_to_movies(json.loads(str(r)))
        return movies

