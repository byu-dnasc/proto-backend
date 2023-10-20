def test_ingest(index_f, movies_f):
    index_f.blocking_ingest(movies_f)
    movies = index_f.get_movies()
    assert movies

def test_get_latest_movie_update(index_f, movies_f):
    index_f.blocking_ingest(movies_f)
    ts = index_f.get_latest_movie_update()
    ts = sorted([m.updated_at for m in movies_f])[-1]
    assert ts == ts

def test_get_movies(load_index_f, index_f, movie_ids_f):
    load_index_f
    movies = index_f.get_movies(ids=movie_ids_f)
    assert len(movies) == len(movie_ids_f)