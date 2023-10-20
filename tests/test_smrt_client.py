import smrtlink.client

def test_set_analysis_types(senarios_f):
    senario = senarios_f['set_analysis_types']
    analyses = [smrtlink.datasets.Analysis(a) for a in senario['analysis_json']]
    assert all([a for a in analyses if a.type == smrtlink.datasets.Analysis.DEFAULT_TYPE])
    jobs = senario['jobs_json']
    smrtlink.client.set_analysis_types(analyses, jobs)
    assert not any([a for a in analyses if a.type == smrtlink.datasets.Analysis.DEFAULT_TYPE])