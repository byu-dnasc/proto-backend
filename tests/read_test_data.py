import json

import smrtlink.client
import smrtlink.datasets

def get_jobs_json():
    with open('tests/json/jobs.json', 'r') as f:
        return json.load(f)

def get_analysis_jobs(analyses, jobs_json):
    '''Filter jobs to only those that are associated with the given analyses.'''
    analysis_job_ids = [a.job_id for a in analyses if a.type == smrtlink.datasets.Analysis.DEFAULT_TYPE]
    return [j for j in jobs_json if j['id'] in analysis_job_ids]

def get_senarios():
    with open('tests/json/senarios.json', 'r') as f:
        return json.load(f)

def get_datasets_by_movie_id():
    with open('tests/json/datasets.json', 'r') as f:
        dataset_json = json.load(f)
    movie_datasets_by_id = {}
    jobs_json = get_jobs_json()
    for movie_id, movie_datasets_json in dataset_json.items():
        ccsreads = sorted(movie_datasets_json['ccsreads'], key=lambda d: d['importedAt'])
        analyses, samples = smrtlink.client.differentiate(ccsreads)
        jobs = get_analysis_jobs(analyses, jobs_json)
        smrtlink.client.set_analysis_types(analyses, analysis_jobs=jobs)
        subreads_json = movie_datasets_json['subreads']
        if subreads_json:
            subreads = [smrtlink.datasets.Subreads(subreads_j) for subreads_j in subreads_json]
            movie_datasets_by_id[movie_id] = subreads + analyses + samples
        else:
            movie_datasets_by_id[movie_id] = analyses + samples
    return movie_datasets_by_id

def get_movies():
    with open('tests/json/movies.json', 'r') as f:
        return json.load(f)