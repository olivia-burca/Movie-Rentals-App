from datetime import *
from random import randint,choice

from domain.client import ClientValidator
from domain.movie import MovieValidator
from domain.rental import Rental, RentalValidationException, RentalValidator
from repository.clientRepo import ClientRepository
from repository.movieRepo import MovieRepository
from repository.rentalRepo import RentalRepository
from service.clientFunct import ClientFunctionalities
from service.movieFunct import MovieFunctionalities
from service.undoService import FunctionCall, Operation, CascadedOperation
from iterable import Iterable, combSort, filter

class RentalService:
    def __init__(self, rental_repo:RentalRepository, movie_repo:MovieRepository, client_repo:ClientRepository,rental_validator:RentalValidator,undo_service,rented_movies):
        self._rental_repo = rental_repo
        self._movie_repo = movie_repo
        self._client_repo = client_repo
        self._validator = rental_validator
        self._undo_service = undo_service
        self._rented_movies = rented_movies.copy()

    @property
    def rented_movies(self):
        return self._rented_movies

    @property
    def rental_repo(self):
        return self._rental_repo

    @property
    def rental_validator(self):
        return self._validator

    @property
    def movie_repo(self):
        return self._movie_repo

    @property
    def client_repo(self):
        return self._client_repo

    def add_rental(self, rental):
        today = date.today()
        found = False
        for c in self.client_repo:
            if c.client_id == rental.client_id:
                found = True
        if not found:
            raise ValueError('The client with the given ID does not exist!')
        found = False
        for m in self.movie_repo:
            if m.movie_id == rental.movie_id:
                found = True
        if not found:
            raise ValueError('The movie with the given ID does not exist!')

        if rental.rented_date > rental.due_date:
            raise ValueError('Rented date cannot be after due date!')
        for r in self._rental_repo:
            if r.rental_id == rental.rental_id:
                raise ValueError('Duplicate id!')
            if r.client_id == rental.client_id:
                if r.returned_date=='Not returned yet':
                    if r.due_date < today:
                        raise ValueError('This client cannot rent another movie, because they have one or '
                                         'more rented movies that passed their due date for return')
                elif r.returned_date > r.due_date:
                    raise ValueError('This client cannot rent another movie, because they have one or '
                                     'more rented movies that passed their due date for return')

        try:
            self.update_rental_repo()
            self.rental_validator.validate(rental)
            self._rental_repo.add_rental(rental)
            undo_op = FunctionCall(self._rental_repo.delete_rental,rental)
            redo_op = FunctionCall(self._rental_repo.add_rental,rental)
            op = Operation(undo_op,redo_op)
            self._undo_service.record(op)

        except RentalValidationException as rve:
            print(str(rve))

        for m in self.movie_repo:
            if m.movie_id == rental.movie_id :
                self.rented_movies.append(m)
                self.movie_repo.remove_movie(m)


    def return_movie(self, id, returned_d):
        found = False
        for r in self._rental_repo:

            if int(r.rental_id) == int(id):
                found = True
                rental = r

                if returned_d < r.rented_date:
                    raise ValueError('The returned date cannot be earlier than the rented date!')

                self.update_rental_repo()
                self._rental_repo.return_movie(id,returned_d)
                undo_op = FunctionCall(self.rental_repo.return_movie, rental.rental_id, 'Not returned yet')
                redo_op = FunctionCall(self._rental_repo.return_movie,r.rental_id,r.returned_date)
                op = Operation(undo_op,redo_op)
                self._undo_service.record(op)

                for m in self.rented_movies:
                    if m.movie_id == r.movie_id:
                        self.rented_movies.remove(m)
                        self.movie_repo.add_movie(m)

        if not found:
            raise ValueError('Rental with given ID does not exist!')


    def update_rental_repo(self):
        new=[]
        found = False
        for rental in self.rental_repo:
            found = False
            c = self._client_repo.search_by_id(rental.client_id)
            for movie in self._rented_movies:
                if movie.movie_id == rental.movie_id:
                    m = movie

            if c is None:
                self._rental_repo.return_movie(rental.rental_id,date.today())
                undo_op = FunctionCall(self.rental_repo.return_movie,rental.rental_id,'Not returned yet')
                redo_op = FunctionCall(self.rental_repo.return_movie,rental.rental_id,date.today())
                op = Operation(undo_op,redo_op)
                new.append(op)

        if self._undo_service.return_index()>-1:
            if self._undo_service.normal_operation():
                op1, op2 = self._undo_service.separate_last_op()
                if op1.function_ref() == self._client_repo.add_client and op2.function_ref() == self._client_repo.remove_client:
                    op = Operation(op1, op2)
                    c_op = CascadedOperation(op, *new)
                    self._undo_service.remove_last_element()
                    self._undo_service.record(c_op)
        return None

    def get_all(self):
        self.update_rental_repo()
        return self._rental_repo.get_all()




    def filter_rentals(self, client, movie):
        """
        Return a list of rentals performed by the provided client for the provided car
        client - The client performing the rental. None means all clients
        movie - The rented movie. None means all movies

        """
        '''
        result = []
        if client is not None:
            result = filter(self.rental_repo, lambda rental:  rental.client_id!= client.client_id)

        if movie is not None:
            result = filter(self.rental_repo, lambda rental: rental.movie_id != movie.movie_id)
        '''
        result = []
        for rental in self.rental_repo:
            if client is not None and rental.client_id != client.client_id:
                continue
            if movie is not None and rental.movie_id != movie.movie_id:
                continue
            result.append(rental)

        return result

    def create_movie_rental_day_count(self,movie):
        days = timedelta()
        for r in self.rental_repo:
            if r.movie_id == movie.movie_id:
                if r.returned_date == 'Not returned yet':
                    days = days + date.today() - r.rented_date

                else:
                    days = days + r.returned_date - r.rented_date
        return days

    def most_rented_movies(self):
        result = []
        for movie in self.rented_movies:
            drc = DaysRentalCountMovie(movie, self.create_movie_rental_day_count(movie))
            result.append(drc)
        combSort(result, lambda m1,m2: m1.days_count < m2.days_count )

        return result

    def create_movie_day_delay_count(self, movie):
        days = timedelta()
        for r in self.rental_repo:
            if r.movie_id == movie.movie_id:
                if r.due_date < date.today() and r.returned_date == 'Not returned yet':
                    days = days + date.today() - r.due_date

        return days

    def late_rentals(self):
        result = []
        for movie in self.rented_movies:
            dd = DaysOfDelay(movie, self.create_movie_day_delay_count(movie))
            if dd.days_count != timedelta():
                result.append(dd)
        combSort(result, lambda m1, m2: m1.days_count < m2.days_count)

        return result

    def create_client_rental_day_count(self,client):
        days = timedelta()
        for r in self.filter_rentals(client,None):
            if r.returned_date == 'Not returned yet':
                days = days + date.today() - r.rented_date

            else:
                days = days + r.returned_date - r.rented_date

        return days

    def most_active_clients(self):
        result = []
        for client in self.client_repo:
            drc = DaysRentalCountClient(client, self.create_client_rental_day_count(client))
            if drc.days_count != timedelta():
                result.append(drc)
        combSort(result, lambda c1, c2: c1.days_count < c2.days_count)

        return result

class DaysRentalCountMovie:
    def __init__(self,movie,days_count):
        self._movie = movie
        self._days_count = days_count

    @property
    def movie(self):
        return self._movie

    @property
    def days_count(self):
        return self._days_count

    def __str__(self):
        return str(self.movie) + '\n' + ' '*150 + str(self.days_count)


class DaysRentalCountClient:
    def __init__(self,client,days_count):
        self._client = client
        self._days_count = days_count

    @property
    def client(self):
        return self._client

    @property
    def days_count(self):
        return self._days_count

    def __str__(self):
        return str(self.client) + '\n' + ' '*150 + str(self.days_count)

class DaysOfDelay:
    def __init__(self,movie,days_count):
        self._movie = movie
        self._days_count = days_count

    @property
    def movie(self):
        return self._movie

    @property
    def days_count(self):
        return self._days_count

    def __str__(self):
        return str(self.movie) + '\n' + ' '*150 + str(self.days_count)