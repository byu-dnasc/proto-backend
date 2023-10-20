import json

import smrtlink.client
import smrtlink.movies
import smrtlink.datasets
import smrtlink.utils

class TestSmrtClient(smrtlink.client.SmrtClient):
    def get_subreads_by_movie_id(self, movie_id): 
        subreads_json = smrtlink.utils.get_endpoint(f'/datasets/subreads?metadataContextId={movie_id}', self._get_token())
        return subreads_json
    def get_ccsreads_by_movie_id(self, movie_id):
        ccsreads_json = smrtlink.utils.get_endpoint(f'/datasets/ccsreads?metadataContextId={movie_id}', self._get_token())
        return ccsreads_json
    def get_ccsreads_json(self):
        ccsreads_json = smrtlink.utils.get_endpoint(f'/datasets/ccsreads', self._get_token())
        return ccsreads_json

def get_movies(subreads_json, ccsreads_json):
    datasets = get_datasets(subreads_json, ccsreads_json)
    return smrtlink.movies.get_new_movies(datasets)
    
def write_movies_file(movies):
    with open('tests/json/movies_tmp.json', 'w') as f:
        movies_by_id = {m.id: m.to_dict() for m in movies}
        json.dump(movies_by_id, f, indent=4)

def write_datasets_file(subreads_json_by_movie_id, ccsreads_json_by_movie_id):
    with open('tests/json/datasets_tmp.json', 'w') as f:
        datasets_by_movie_id = {
            id: {
                'subreads': subreads_json_by_movie_id[id],
                'ccsreads': ccsreads_json_by_movie_id[id]
            }
            for id in subreads_json_by_movie_id.keys()
        }
        json.dump(datasets_by_movie_id, f, indent=4)

def get_analysis_jobs(movies, subreads_json_by_movie_id, ccsreads_json_by_movie_id):
    movie_ids = [m.id for m in movies]
    datasets_by_movie_id = { 
        id: get_datasets
        (
            subreads_json_by_movie_id[id], 
            ccsreads_json_by_movie_id[id]
        ) 
        for id in movie_ids
    }
    jobs = []
    for movie in movies:
        analysis_dataset_ids = [a['dataset_id'] for a in movie.analyses]
        movie_datasets_by_id = {ds.id: ds for ds in datasets_by_movie_id[movie.id]}
        analyses = [movie_datasets_by_id[id] for id in analysis_dataset_ids]
        jobs += smrtlink.client.get_analysis_jobs([a.job_id for a in analyses])
    return jobs

def write_jobs_file(jobs):
    with open('tests/json/jobs_tmp.json', 'w') as f:
        json.dump(jobs, f, indent=4)

def get_datasets(subreads_json, ccsreads_json):
    subreads_datasets = [smrtlink.datasets.Subreads(j) for j in subreads_json]
    analysis_datasets, sample_datasets = smrtlink.client.differentiate(ccsreads_json)
    smrtlink.client.set_analysis_types(analysis_datasets)
    return subreads_datasets[::-1] + analysis_datasets[::-1] + sample_datasets[::-1]

def main(movie_ids):
    subreads_json_by_movie_id = {id: TestSmrtClient().get_subreads_by_movie_id(id) for id in movie_ids}
    ccsreads_json_by_movie_id = {id: TestSmrtClient().get_ccsreads_by_movie_id(id) for id in movie_ids}
    movies = get_movies(
        [ds for sublist in subreads_json_by_movie_id.values() for ds in sublist],
        [ds for sublist in ccsreads_json_by_movie_id.values() for ds in sublist]
    )
    jobs = get_analysis_jobs(movies, subreads_json_by_movie_id, ccsreads_json_by_movie_id)
    write_datasets_file(subreads_json_by_movie_id, ccsreads_json_by_movie_id)
    write_movies_file(movies)
    write_jobs_file(jobs)

if __name__ == '__main__':
    movie_ids = ['m84100_230808_191706_s1', 'm54336U_230916_093547', 'm54336U_231006_215609']
    main(movie_ids)