import json
import time

from smrtlink.datasets import SmrtLinkDataset, Sample, Analysis, Subreads

_representative_analysis_types = [Analysis.CCS_TYPE, Analysis.DEMUX_TYPE, Analysis.IMPORT_TYPE]

class MovieJson:
    '''
    Similar purpose to MovieBuilder, but consists of a dictionary of movie data rather
    than dataset objects. This makes it easy to ingest into Globus Search.
    '''
    def __init__(self, movie_json: dict):
        if 'ingested_at' in movie_json.keys():
            del movie_json['ingested_at']
        self.__dict__ = movie_json
   
    def __str__(self):
        return json.dumps(self.__dict__, indent=4)
    
    def to_dict(self): # to prepare object for json.dumps
        self.__dict__['ingested_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
        return self.__dict__
    
    def __eq__(self, movie_json) -> bool:
        if not isinstance(movie_json, MovieJson):
            raise Exception('Cannot compare MovieJson to ' + str(type(movie_json)))
        return self.__dict__ == movie_json.__dict__
    
    def add(self, dataset):
        '''
        Update the movie json with a new dataset.
        '''
        if dataset.created_at > self.updated_at:
            self.updated_at = dataset.created_at
        if isinstance(dataset, Sample):
            sample_demux_analysis = [a for a in self.analyses if a['dataset_uuid'] == dataset.demux_dataset_uuid][0]
            sample_demux_analysis['samples'].append(dataset.to_dict())
        elif isinstance(dataset, Analysis):
            self.analyses.append(dataset.to_dict())
            if dataset.type in _representative_analysis_types:
                self.hifi_metrics = dataset.get_hifi_metrics()
    
def _get_demux_analysis(analysis, samples):
    analysis_samples = [s for s in samples if s.demux_dataset_uuid == analysis.uuid]
    return analysis.to_dict(sorted(analysis_samples, key=lambda s: s.barcode_name))

def _analyses_to_array(analyses, samples):
    analysis_dicts = []
    for analysis in analyses:
        if analysis.type == Analysis.DEMUX_TYPE:
            analysis_dicts.append(_get_demux_analysis(analysis, samples))
        else:
            analysis_dicts.append(analysis.to_dict())
    return analysis_dicts

class MovieBuilder:
    '''
    Class to build a MovieJson object when none exists yet.
    As opposed to MovieJson, this class handles Subreads datasets 
    and movie metadata.
    '''
    def __init__(self, dataset: SmrtLinkDataset):
        self.samples = []
        self.analyses = []
        self.subreads_metrics = None
        self.movie_metadata = dataset.get_movie_metadata()
        self.updated_at = '' # the timestamp of the most recent dataset
        self.hifi_metrics = None
        self.add(dataset)
    
    def add(self, dataset):
        if dataset.created_at > self.updated_at:
            self.updated_at = dataset.created_at
        if isinstance(dataset, Sample):
            self.samples.append(dataset)
        elif isinstance(dataset, Analysis):
            self.analyses.append(dataset)
            # exploit the assumption that datasets are ordered chronologically.
            if dataset.type in _representative_analysis_types:
                self.hifi_metrics = dataset.get_metrics()
        elif isinstance(dataset, Subreads):
            self.subreads_metrics = dataset.to_dict()
        else:
            raise Exception('Unknown dataset type: ' + str(type(dataset)))
        return self
    
    def to_movie_json(self):
        j = {
            'analyses': _analyses_to_array(self.analyses, self.samples),
            'hifi_metrics': self.hifi_metrics,
            'subreads_metrics': self.subreads_metrics
        }
        j.update(self.movie_metadata)
        j.update({'updated_at': self.updated_at})
        return MovieJson(j)
    
def get_new_movies(datasets):
    '''Create MovieJson objects from datasets of movies which have not been seen before.'''
    movie_builders = {}
    for dataset in datasets:
        if dataset.movie_id in movie_builders.keys():
            movie_builders[dataset.movie_id].add(dataset) 
        else:
            new_movie = MovieBuilder(dataset)
            movie_builders[dataset.movie_id] = new_movie
    return [movie_builder.to_movie_json() for movie_builder in list(movie_builders.values())]

def update_movies(movies, datasets):
    '''Update MovieJson objects with new datasets.'''
    movie_jsons = {movie.id: movie for movie in movies}
    for dataset in datasets:
        movie_jsons[dataset.movie_id].add(dataset)
    return list(movie_jsons.values())