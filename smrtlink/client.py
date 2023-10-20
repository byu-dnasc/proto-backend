import urllib3

from smrtlink.auth import TokenManager
from smrtlink.datasets import Subreads, Sample, Analysis
from smrtlink.utils import get_endpoint, post_endpoint

def set_analysis_types(analyses, analysis_jobs=None):
    '''
    param analyses: a list of Analysis objects (intended for testing)
    The analysis jobs parameter must consist only of 
    jobs that are associated with the given analyses.
    Otherwise, you will get a KeyError.
    '''
    job_to_analysis = {a.job_id: a.id for a in analyses if a.type == Analysis.DEFAULT_TYPE}
    # get jobs for analysis datasets
    if not analysis_jobs:
        analysis_jobs = get_analysis_jobs(job_to_analysis.keys())
    # set analysis types
    analyses_by_id = {a.id: a for a in analyses}
    for job in analysis_jobs:
        analysis_id = job_to_analysis[job['id']]
        analyses_by_id[analysis_id].set_type(job)

def differentiate(ccsreads_json):
    # create analyses and samples
    sample_datasets = []
    analysis_datasets = {}
    for dataset in ccsreads_json:
        if 'parentUuid' in dataset.keys():
            sample_datasets.append(Sample(dataset))
        else:
            dataset_id = dataset['uuid']
            if dataset['numChildren'] > 0:
                analysis_datasets[dataset_id] = Analysis(dataset, type=Analysis.DEMUX_TYPE)
            else:
                analysis_datasets[dataset_id] = Analysis(dataset)
    return list(analysis_datasets.values()), sample_datasets

class SmrtClient:

    # singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SmrtClient, cls).__new__(cls)
            cls.instance._initialize()
        return cls.instance

    def _initialize(self):
        # verify that the server is accessible
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # see _get_endpoint
        try: 
            self.get_server_status()
        except Exception as e:
            raise Exception('Failed to create SmrtClient: ' + str(e))
        # initialize
        try:
            self.token_manager = TokenManager()
        except Exception as e:
            raise Exception('Failed to create SmrtClient: ' + str(e))

    def _get_token(self):
        return self.token_manager.get_token()
    
    def get_server_status(self):
        return get_endpoint('/status', None)

    def get_datasets_created_after(self, timestamp: str):
        '''
        Get all datasets created after the timestamp parameter. 
        Datasets are ordered by two rules:
        Subreads first, Analyses second, Samples third. 
        Ascending chronological order.
        '''
        subreads_json = get_endpoint(f'/datasets/subreads?importedAt=gt%3A{timestamp}', self._get_token())
        ccsreads_json = get_endpoint(f'/datasets/ccsreads?importedAt=gt%3A{timestamp}', self._get_token())
        subreads_datasets = [Subreads(j) for j in subreads_json]
        analysis_datasets, sample_datasets = differentiate(ccsreads_json)
        set_analysis_types(analysis_datasets)
        return subreads_datasets[::-1] + analysis_datasets[::-1] + sample_datasets[::-1]

    def get_analysis_jobs(self, job_ids):
        ids = {'id': 'in:' + ','.join([str(id) for id in job_ids])}
        j = post_endpoint(f'/job-manager/jobs/analysis/search', self._get_token(), ids)
        return j
    
def get_datasets_created_after(timestamp: str):
    return SmrtClient().get_datasets_created_after(timestamp)

def get_analysis_jobs(job_ids):
    return SmrtClient().get_analysis_jobs(job_ids)