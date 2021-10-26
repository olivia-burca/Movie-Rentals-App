from domain.movie import MovieValidationException, MovieValidator
from repository.movieRepo import MovieRepository
from service.undoService import FunctionCall, Operation
from iterable import filter

class MovieFunctionalities:

    def __init__(self,movie_repo:MovieRepository, movie_validator:MovieValidator,undo_service):
        self._repo = movie_repo
        self._validator = movie_validator
        self._undo_service = undo_service

    @property
    def movie_repo(self):
        return self._repo

    @property
    def movie_validator(self):
        return self._validator


    def add_movie(self,movie):
        for m in self._repo:
            if m.movie_id == movie.movie_id :
                raise ValueError('Duplicate id!')

        try:
            self.movie_validator.validate(movie)
            self._repo.add_movie(movie)
            undo_op = FunctionCall(self._repo.remove_movie, movie)
            redo_op = FunctionCall(self._repo.add_movie, movie)
            op = Operation(undo_op, redo_op)
            self._undo_service.record(op)
        except MovieValidationException as mve:
            print(str(mve))


    def remove_movie(self,id):
        found = False
        for m in self._repo:
            if m.movie_id == id:
                found = True
                movie = self._repo.search_by_id(id)
                self._repo.remove_movie(m)
                undo_op = FunctionCall(self._repo.add_movie, movie)
                redo_op = FunctionCall(self._repo.remove_movie, movie)
                op = Operation(undo_op, redo_op)
                self._undo_service.record(op)
        if not found:
            raise ValueError('Movie with given ID does not exist!')

    def update_movie(self,id,key,new):
        found = False
        for m in self._repo:
            if m.movie_id == id:
                found = True
                movie = self._repo.search_by_id(id)
                init_title = movie.title
                init_id = movie.movie_id
                init_genre = movie.genre
                init_description = movie.description
                if key == 'title':
                    self._repo.update_title_movie(id, new)
                    undo_op = FunctionCall(self._repo.update_title_movie, id, init_title)
                    redo_op = FunctionCall(self._repo.update_title_movie, id, new)
                    op = Operation(undo_op, redo_op)
                    self._undo_service.record(op)
                elif key == 'id':
                    self._repo.update_id_movie(id, new)
                    undo_op = FunctionCall(self._repo.update_id_movie, id, init_id)
                    redo_op = FunctionCall(self._repo.update_id_movie, id, new)
                    op = Operation(undo_op, redo_op)
                    self._undo_service.record(op)
                elif key == 'description':
                    self._repo.update_description_movie(id, new)
                    undo_op = FunctionCall(self._repo.update_description_movie, id, init_description)
                    redo_op = FunctionCall(self._repo.update_description_movie, id, new)
                    op = Operation(undo_op, redo_op)
                    self._undo_service.record(op)
                elif key == 'genre':
                    self._repo.update_genre_movie(id, new)
                    undo_op = FunctionCall(self._repo.update_genre_movie, id, init_genre)
                    redo_op = FunctionCall(self._repo.update_genre_movie, id, new)
                    op = Operation(undo_op, redo_op)
                    self._undo_service.record(op)
                else:
                    raise ValueError('You can only update the id, the title, the description or the genre! ')
        if not found:
            raise ValueError('Movie with given ID does not exist!')

    def search_movie(self, key, word):
        result = []
        if key == 'id':
            result = filter(self.movie_repo, lambda m: word in m.movie_id)
        elif key == 'title':
            result = filter(self.movie_repo, lambda m: word in m.title)
        elif key == 'description':
            result = filter(self.movie_repo, lambda m: word in m.description)
        elif key == 'genre':
            result = filter(self.movie_repo, lambda m: word in m.genre)
        else:
            raise ValueError('You can only search movies using id, title, description or genre!')

        return result


