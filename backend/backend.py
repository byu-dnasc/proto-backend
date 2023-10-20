from smrtlink.client import SmrtClient
import smrtlink.movies as smrtlink
from globus.index import Index
from backend.utils import *

class Backend:

    def __init__(self, index_id=None):
        self.index = Index(index_id=index_id)
        self.smrt_client = SmrtClient()
    
    def get_new_datasets(self):
        latest_movie_update = self.index.get_latest_movie_update()
        new_datasets = self.smrt_client.get_datasets_created_after(latest_movie_update)
        report_dataset_updates(latest_movie_update, len(new_datasets))
        return new_datasets
    
    def get_movies_to_update(self, new_datasets):
        to_update = [ds.movie_id for ds in new_datasets if not isinstance(ds, smrtlink.Subreads)]
        return self.index.get_movies(ids=to_update)
    
    def update_index(self):
        new_datasets = self.get_new_datasets()
        movies_to_update = self.get_movies_to_update(new_datasets)
        existing_movie_ids = [m.id for m in movies_to_update]
        # split datasets
        new_movie_datasets      = [ds for ds in new_datasets if ds.movie_id not in existing_movie_ids]
        existing_movie_datasets = [ds for ds in new_datasets if ds.movie_id     in existing_movie_ids]
        # get movies
        new_movies = smrtlink.get_new_movies(new_movie_datasets)
        updated_movies = smrtlink.update_movies(movies_to_update, existing_movie_datasets)
        self.index.blocking_ingest(new_movies + updated_movies)