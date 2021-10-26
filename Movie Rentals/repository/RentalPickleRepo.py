import pickle

from repository.rentalRepo import RentalRepository


class RentalPickleRepository(RentalRepository):

    def __init__(self,file_name,rented_movies):
        super().__init__([],rented_movies)
        self._file_name = file_name
        self._rented_movies = rented_movies
        self._load()

    def _save(self):
        f = open(self._file_name,'wb')
        pickle.dump(self._rental_list,f)
        f.close()

    def _load(self):
        result = []
        try:
            f = open(self._file_name,'rb')
            self._rental_list = pickle.load(f)
            f.close()
            return self._rental_list
        except EOFError:
            return result
        except IOError as e:
            raise e

    def add_rental(self, rental):
        super().add_rental(rental)
        self._save()

    def delete_rental(self, rental):
        super().delete_rental(rental)
        self._save()

    def return_movie(self, id, returned_d):
        super().return_movie(id, returned_d)
        self._save()