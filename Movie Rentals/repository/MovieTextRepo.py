from domain.movie import Movie
from repository.movieRepo import MovieRepository


class MovieTextFileRepository(MovieRepository):


    def __init__(self, file_name='movies.txt'):
        super().__init__([])
        self._file_name = file_name
        self._load()

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

    def _save(self):
        f = open(self._file_name, 'wt')
        for movie in self._movie_list:
            line = str(movie.movie_id) + ';' + movie.title + ';' + movie.description + ';' + movie.genre
            f.write(line)
            f.write('\n')
        f.close()

    def _load(self):

        f = open(self._file_name, 'rt')  # read text
        lines = f.readlines()
        f.close()

        for line in lines:
            line = line.split(';')
            super().add_movie(Movie(line[0], line[1] , line[2], line[3] ))