class SmrtLinkDataset:
    '''Not intended to be instantiated.'''

    def __init__(self, dataset):
        # TODO: rename fields in context of DNASC App
        self.created_at = dataset['importedAt']
        self.id = dataset['id']
        self.uuid = dataset['uuid']
        self.num_bases = dataset['totalLength']
        self.num_reads = dataset['numRecords']
        self.project_id = dataset['projectId']
        self.instrument = dataset['instrumentName']
        self.run_name = dataset['wellSampleName']
        self.cell_id = str(dataset['cellIndex'] + 1) + '_' + dataset['wellName']
        self.batch_name = dataset['runName']
        self.movie_id = dataset['metadataContextId']
        self.job_id = dataset['jobId'] # the id of the job that created this dataset
   
    def get_movie_metadata(self):
        return {
            'project_id': self.project_id,
            'instrument': self.instrument,
            'run_name': self.run_name,
            'cell_id': self.cell_id,
            'batch_name': self.batch_name,
            'id': self.movie_id,
        }
   
class Sample(SmrtLinkDataset):
    def __init__(self, dataset):
        super().__init__(dataset)
        self.sample_name = dataset['bioSampleName']
        self.barcode_name = dataset['dnaBarcodeName']
        self.demux_dataset_uuid = dataset['parentUuid']
        self.matched_to_analysis = False
    
    def to_dict(self):
        return {
            'sample_name': self.sample_name,
            'barcode_name': self.barcode_name,
            'num_reads': self.num_reads,
            'num_bases': self.num_bases,
            'dataset_id': self.id
        }

class Analysis(SmrtLinkDataset):
    CCS_TYPE = 'Circular Consensus Sequencing'
    DEMUX_TYPE = 'Demultiplex Reads'
    IMPORT_TYPE = 'Import from file'
    DEFAULT_TYPE = IMPORT_TYPE

    def __init__(self, dataset, type=None):
        super().__init__(dataset)
        self.type = type if type else Analysis.IMPORT_TYPE
    
    def set_type(self, analysis_job: dict):
        if analysis_job['subJobTypeId'] == 'cromwell.workflows.pb_ccs':
            self.type = Analysis.CCS_TYPE
        else:
            self.type = analysis_job['applicationName']

    def to_dict(self, samples=None):
        d = {
            'type': self.type,
            'num_reads': self.num_reads,
            'num_bases': self.num_bases,
            'dataset_id': self.id,
            'dataset_uuid': self.uuid
        }
        if samples is not None:
            d['samples'] = [s.to_dict() for s in samples]
            d.pop('num_reads')
            d.pop('num_bases')
        return d
    
    def get_metrics(self):
        return {
            'num_reads': self.num_reads,
            'num_bases': self.num_bases,
            'dataset_id': self.id
        }

class Subreads(SmrtLinkDataset):
    '''
    There is only ever one Subreads dataset (if any) per movie 
    and it will always be the movie's earliest dataset.
    '''
    def __init__(self, dataset):
        super().__init__(dataset)
    
    def to_dict(self):
        return {
            'num_reads': self.num_reads,
            'num_bases': self.num_bases,
            'dataset_id': self.id
        }

