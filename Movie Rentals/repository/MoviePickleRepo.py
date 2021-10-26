import pickle

from repository.movieRepo import MovieRepository


class MoviePickleRepository(MovieRepository):

    def __init__(self,file_name):
        super().__init__([])
        self._file_name = file_name
        self._load()

    def _save(self):
        f = open(self._file_name,'wb')
        pickle.dump(self._movie_list,f)
        f.close()

    def _load(self):
        result = []
        try:

            f = open(self._file_name,'rb')
            self._movie_list = pickle.load(f)
            f.close()
            return self._movie_list
        except EOFError:
            return result
        except IOError as e:
            raise e

    def add_movie(self,movie):
        super().add_movie(movie)
        self._save()

    def remove_movie(self,movie):
        super().remove_movie(movie)
        self._save()

    def update_id_movie(self, id, new):
        super().update_id_movie(id,new)
        self._save()

    def update_title_movie(self, id, new):
        super().update_title_movie(id,new)
        self._save()

    def update_description_movie(self, id, new):
        super().update_description_movie(id,new)
        self._save()

    def update_genre_movie(self, id, new):
        super().update_genre_movie(id, new)
        self._save()