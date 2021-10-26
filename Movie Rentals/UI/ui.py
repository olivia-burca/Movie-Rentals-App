from datetime import date
from domain.client import Client, ClientValidator
from domain.rental import Rental, RentalValidator
from repository.clientRepo import ClientRepository
from repository.rentalRepo import RentalRepository
from service.clientFunct import ClientFunctionalities
from domain.movie import Movie, MovieValidator
from repository.movieRepo import MovieRepository
from service.movieFunct import MovieFunctionalities
from service.rentalFunct import RentalService
from service.undoService import UndoService


class UI:

    def __init__(self,client_service,movie_service,rental_service,undo_service):
        self._client_service = client_service
        self._movie_service = movie_service
        self._rental_service = rental_service
        self._undo_service = undo_service

    @property
    def client_service(self):
        return self._client_service

    @property
    def movie_service(self):
        return self._movie_service

    @property
    def rental_service(self):
        return self._rental_service


    def print_menu(self):
        print('1.Add a client')
        print('2.Remove a client')
        print('3.Update a client')
        print('4.List the clients')
        print('5.Add a movie')
        print('6.Remove a movie')
        print('7.Update a movie')
        print('8.List the movies')
        print('9.Rent a movie')
        print('10.Return a movie')
        print('11.List rentals')
        print('12.Search clients')
        print('13.Search movies')
        print('14.Most rented movies')
        print('15.Most active clients')
        print('16.Late rentals')
        print('17.Undo')
        print('18.Redo')
        print('0.Exit')



    def create_client(self):
        client_id = input('Enter the client id: ')
        if not isinstance(client_id,str):
            raise ValueError('ID should be a string')
        name = input('Enter the client name: ')
        if not isinstance(name,str):
            raise ValueError('Name should be a string')
        return Client(client_id,name)

    def create_movie(self):
        movie_id = input('Enter the movie id: ')
        if not isinstance(movie_id,str):
            raise ValueError('ID should be a string')
        title = input('Enter the movie title: ')
        if not isinstance(title,str):
            raise ValueError('Title should be a string')
        description = input('Enter the movie description: ')
        if not isinstance(description, str):
            raise ValueError('Description should be a string')
        genre = input('Enter the movie genre: ')
        if not isinstance(genre, str):
            raise ValueError('Genre should be a string')

        return Movie(movie_id,title,description,genre)

    def create_rental(self):
        rental_id = input('Enter rental id: ')
        movie_id = input('Enter the movie id: ')
        client_id = input('Enter the client id: ')
        d1, m1, y1 = [int(x) for x in input("Enter rented date(DD/MM/YYYY) : ").split('/')]
        rented_date = date(y1,m1,d1)
        d2, m2, y2 = [int(x) for x in input("Enter due date(DD/MM/YYYY) : ").split('/')]
        due_date = date(y2,m2,d2)
        return Rental(rental_id,movie_id,client_id,rented_date,due_date)


    def add_client_ui(self):
        client = self.create_client()
        self._client_service.add_client(client)

    def add_movie_ui(self):
        movie = self.create_movie()
        self._movie_service.add_movie(movie)

    def remove_client_ui(self):
        id = input('Enter the id of the client that you want to remove: ')
        self._client_service.remove_client(id)

    def remove_movie_ui(self):
        id = input('Enter the id of the movie that you want to remove: ')
        self._movie_service.remove_movie(id)

    def update_client_ui(self):
        id = input('Enter the id of the client that you want to update: ')
        key = input('What do you want to update: ')
        new = input('Enter the new attribute: ')
        self._client_service.update_client(id,key,new)

    def update_movie_ui(self):
        id = input('Enter the id of the movie that you want to update: ')
        key = input('What do you want to update: ')
        new = input('Enter the new attribute: ')
        self._movie_service.update_movie(id,key,new)

    def add_rental_ui(self):
        rental = self.create_rental()
        self._rental_service.add_rental(rental)

    def return_movie_ui(self):
        id = input('Enter the id of the rental with the movie that you want to return: ')
        d,m,y = [int(x) for x in input("Enter when was the movie returned (DD/MM/YYYY) : ").split('/')]
        returned_date = date(y,m,d)
        self._rental_service.return_movie(id,returned_date)

    def list_clients_ui(self):
        for c in self._client_service.client_repo:
            print(str(c))

    def list_movies_ui(self):
        for m in self._movie_service.movie_repo:
            print(str(m))

    def list_rentals_ui(self):
    #    for r in self._rental_service.rental_repo:
    #        print(str(r))

        for r in self._rental_service.get_all():
            print(str(r))

    def search_client_ui(self):
        key = input('Enter what you want to search clients by (id/name): ')
        word = input('Enter the string: ')
        l = self._client_service.search_client(key,word)
        if len(l) == 0:
            print('No clients with ' + str(word) + ' in '+ str(key))
        else:
            for c in l:
                print(str(c))

    def search_movie_ui(self):
        key = input('Enter what you want to search movies by (id/title/description/genre): ')
        word = input('Enter the string: ')
        l = self._movie_service.search_movie(key,word)
        if len(l) == 0:
            print('No movies with ' + str(word) + ' in '+ str(key))
        else:
            for m in l:
                print(str(m))

    def most_rented_movies_ui(self):
        print("Movie".ljust(10) +' '*137+ " Days".ljust(40))
        print('\n')
        for m in self._rental_service.most_rented_movies():
            print(m)

        print("-" * 70)

    def most_active_clients_ui(self):
        print("Client".ljust(10) + ' ' * 137 + " Days".ljust(40))
        print('\n')
        for c in self._rental_service.most_active_clients():
            print(c)

        print("-" * 70)

    def late_rentals_ui(self):
        print("Movie".ljust(10) +' '*137+ " Days".ljust(40))
        print('\n')
        for m in self._rental_service.late_rentals():
            print(m)

        print("-" * 70)

    def undo_ui(self):
        self._undo_service.undo()

    def redo_ui(self):
        self._undo_service.redo()


    def start(self):
        undo_service = UndoService()
        client_list = []
        client_r = ClientRepository(client_list)
        movie_list = []
        movie_r = MovieRepository(movie_list)
        rental_list = []
        rented_movies = []
        rental_r = RentalRepository(rental_list,rented_movies)

        client_v = ClientValidator()
        movie_v = MovieValidator()
        rental_v = RentalValidator()
        client_service = ClientFunctionalities(client_r,client_v,undo_service)
        movie_service = MovieFunctionalities(movie_r,movie_v,undo_service)
        rental_service = RentalService(rental_r,movie_r,client_r,rental_v,undo_service,rented_movies)
        #rental_service.initialize_rental_list()
        undo_service = UndoService()

        command_dict = {'1': self.add_client_ui, '2': self.remove_client_ui,
                        '3': self.update_client_ui, '4': self.list_clients_ui,
                        '5': self.add_movie_ui, '6':self.remove_movie_ui,
                        '7':self.update_movie_ui, '8':self.list_movies_ui,
                        '9':self.add_rental_ui,'10':self.return_movie_ui,'11':self.list_rentals_ui,
                        '12':self.search_client_ui,'13':self.search_movie_ui,'14':self.most_rented_movies_ui,
                        '15':self.most_active_clients_ui,'16': self.late_rentals_ui,'17':self.undo_ui,'18':self.redo_ui}

        done = False
        while not done:
            self.print_menu()
            command = input('Enter command: ')
            try:
                if command in command_dict:
                    if command in ['1','2','3','4','12']:
                        command_dict[command]()
                    elif command in ['5','6','7','8','13']:
                        command_dict[command]()
                    elif command in ['9','10','11','14','15','16']:
                        command_dict[command]()
                    elif command in ['17','18']:
                        command_dict[command]()
                elif command == '0':
                    done = True
                else:
                    print('Invalid command')
            except ValueError as ve:
                print(str(ve))




