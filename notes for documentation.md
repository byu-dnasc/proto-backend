explain search index refresh


Dataset is 'done' once it's json representation has been created


case 1: A brand new movie is created using a MovieBuilder
case 2: Analyses are added to a movie document

Upon receipt of new datasets:
fetch all movies sharing movie ids with any dataset
if dataset's movie id is among fetched movies: 
    add to movie document
else:
    new = MovieBuilder().add(dataset)


Assumptions that can be made about datasets retrieved from smrt API:

- datasets sorted ~95% in descending order by import timestamp
- Demultiplexing dataset will be created before any of its child datasets

Accommodates the possiblity that a demux analysis' samples become divided between iterations

URI level:

/datasets/subreads?importedAt=gt%3A{}
/datasets/ccsreads?importedAt=gt%3A{}

/datasets/subreads?metadataContextId={}
/datasets/ccsreads?metadataContextId={}

In between:



Client level:

get_datasets_created_after
get_datasets_by_movie_id