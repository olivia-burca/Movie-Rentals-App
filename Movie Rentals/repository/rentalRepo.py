from domain.rental import Rental
from datetime import *
from random import randint,choice

from iterable import Iterable


class RentalRepository:

    def __init__(self,rental_list:Iterable,rented_movies):
        self._rental_list = rental_list[:]
        self._rented_movies = rented_movies.copy()

    @property
    def rental_list(self):
        return self._rental_list

    def get_all(self):
        return self._rental_list[:]

    def add_rental(self,rental):
        if not isinstance(rental, Rental):
            raise TypeError('This is not a rental!')
        self._rental_list.append(rental)

    def delete_rental(self,rental):
        x=0
        if not isinstance(rental,Rental):
            raise TypeError('This is not a rental!')
        for i in range(len(self._rental_list)):
            if self._rental_list[i] == rental:
                x = i

        self._rental_list.__delitem__(x)

    def return_movie(self,id,returned_d):
        for i in range(len(self._rental_list)):
            if self._rental_list[i].rental_id == str(id):
                self._rental_list[i].returned_date = returned_d

    def __getitem__(self, key):
        return self._rental_list[key]

    def __len__(self):
        return len(self._rental_list)


