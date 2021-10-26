from domain.rental import Rental
from repository.rentalRepo import RentalRepository


class RentalTextFileRepository(RentalRepository):



    def __init__(self, file_name, rented_movies):
        super().__init__([],rented_movies)
        self._file_name = file_name
        self._rented_movies = rented_movies
        self._load()

    def add_rental(self,rental):
        super().add_rental(rental)
        self._save()

    def delete_rental(self,rental):
        super().delete_rental(rental)
        self._save()

    def return_movie(self,id,returned_d):
        super().return_movie(id, returned_d)
        self._save()



    def _save(self):
        f = open(self._file_name, 'wt')
        for rental in self._rental_list:
            line = str(rental.rental_id) + ';' + rental.movie_id + ';' + rental.client_id + ';' + str(rental.rented_date) + ';' + str(rental.due_date) + ';' + str(rental.returned_date)
            f.write(line)
            f.write('\n')
        f.close()

    def _load(self):

        f = open(self._file_name, 'rt')  # read text
        lines = f.readlines()
        f.close()

        for line in lines:
            line = line.split(';')
            super().add_rental(Rental(line[0], line[1],line[2],line[3],line[4],line[5]))