from datetime import date


class RentalException(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class RentalValidationException(RentalException):
    def __init__(self, error_list):
        self._errors = error_list

    def __str__(self):
        result = ''

        for er in self._errors:
            result += er
            result += '\n'
        return result


class RentalValidator:
    @staticmethod
    def _is_id_valid(id):
        valid = True
        for i in range(len(id)):
            if not id[i].isdigit():
                valid = False

        return valid


    def validate(self, rental):
        errors = []
        # V1 - All properties are non-empty
        if not self._is_id_valid(rental.rental_id):
            errors.append('Rental ID should only contain digits!')
        if len(str(rental.rented_date)) > 10:
            errors.append('Rented date should have maximum 10 characters!')
        if len(str(rental.due_date)) > 10:
            errors.append('Due date should have maximum 10 characters!')

        if len(errors) > 0:
            raise RentalValidationException(errors)



class Rental:
    def __init__(self,rental_id, movie_id, client_id, rented_date, due_date, returned_date='Not returned yet'):

        self._rental_id = rental_id
        self._movie_id = movie_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._due_date = due_date
        self._returned_date = returned_date

    @property
    def rental_id(self):
        return self._rental_id

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def client_id(self):
        return self._client_id

    @property
    def rented_date(self):
        return self._rented_date

    @property
    def due_date(self):
        return self._due_date

    @property
    def returned_date(self):
        return self._returned_date

    @rental_id.setter
    def rental_id(self, value):
        self._rental_id = value

    @movie_id.setter
    def movie_id(self, value):
        self._movie_id = value

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @rented_date.setter
    def rented_date(self, value):
        self._rented_date = value

    @due_date.setter
    def due_date(self, value):
        self._due_date = value

    @returned_date.setter
    def returned_date(self, value):
        self._returned_date = value

    def __str__(self):
        return 'Rental ID: '+str(self._rental_id) + ', client ID: '+str(self._client_id) + ', movie ID: ' +str(self._movie_id) + '\n Rented date: '+ str(self._rented_date)+ ', due date: '+str(self._due_date)+', returned date: '+str(self._returned_date)

