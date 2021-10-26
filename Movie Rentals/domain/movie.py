class MovieException(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class MovieValidationException(MovieException):
    def __init__(self, error_list):
        self._errors = error_list

    def __str__(self):
        result = ''

        for er in self._errors:
            result += er
            result += '\n'
        return result


class MovieValidator:
    @staticmethod
    def _is_id_valid(id):
        valid = True
        for i in range(len(id)):
            if not id[i].isdigit():
                valid = False

        return valid


    def validate(self, movie):
        errors = []
        # V1 - All properties are non-empty
        if not self._is_id_valid(movie.movie_id):
            errors.append('Movie ID should only contain digits!')
        if len(movie.title) < 3:
            errors.append('Movie title should have at least 3 letters!')
        if len(movie.genre) < 3:
            errors.append('Movie genre should have at least 3 letters!')
        if len(movie.description) < 10:
            errors.append('Movie description should be longer!')


        if len(errors) > 0:
            raise MovieValidationException(errors)



class Movie:
    def __init__(self,movie_id,title,description,genre):
        if not isinstance(movie_id, str):
            raise MovieException('Invalid value for id!')
        if not isinstance(title, str):
            raise MovieException('Invalid title!')
        if not isinstance(genre, str):
            raise MovieException('Invalid genre!')
        if not isinstance(description, str):
            raise MovieException('Invalid description!')

        self._movie_id = movie_id
        self._title = title
        self._description = description
        self._genre = genre

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def genre(self):
        return self._genre

    @movie_id.setter
    def movie_id(self, value):
        self._movie_id = value

    @title.setter
    def title(self, value):
        self._title = value

    @description.setter
    def description(self, value):
        self._description = value

    @genre.setter
    def genre(self, value):
        self._genre = value

    def __str__(self):
        return 'ID: ' + self._movie_id + ', title: ' + self._title + '\n description: ' + self._description + '\n genre: ' + self._genre


