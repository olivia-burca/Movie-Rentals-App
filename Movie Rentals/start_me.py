from datetime import date

from domain.client import ClientValidator, Client
from domain.rental import RentalValidator, Rental
from iterable import Iterable
from repository.ClientPickleRepo import ClientPickleRepository
from repository.ClientTextRepo import ClientTextFileRepository
from repository.MoviePickleRepo import MoviePickleRepository
from repository.MovieTextRepo import MovieTextFileRepository
from repository.RentalPickleRepo import RentalPickleRepository
from repository.RentalTextRepo import RentalTextFileRepository
from repository.clientRepo import ClientRepository
from repository.rentalRepo import RentalRepository
from service.clientFunct import ClientFunctionalities
from domain.movie import MovieValidator, Movie
from repository.movieRepo import MovieRepository
from service.movieFunct import MovieFunctionalities
from service.rentalFunct import RentalService
from UI.ui import UI
from service.undoService import UndoService
from random import choice, randint

from settings import Settings


def initialize_client_list(client_list:Iterable):
    first_name = ['Emilia', 'Alex', 'Andreea', 'Mihai', 'Petru', 'Costel', 'Geanina', 'Diana', 'Mirel', 'Gheorghe']
    last_name = ['Pop', 'Popescu', 'Gireada', 'Apostoliu', 'Iftime', 'Zlampa', 'Ionescu', 'Barbu', 'Vladimirescu','Visinescu']
    for i in range(10):
        id = i + 1
        first = choice(first_name)
        last = choice(last_name)
        name = first + ' ' + last
        client_list.append(Client(str(id), name))
    return client_list


def initialize_movie_list(movie_list):

        titles = ['The Godfather','The Nun','Citizen Kane','2001: A Space Odyssey','Star Wars','Forrest Gump','To kill a mockingbird','Titanic','Clueless','Fast and Furious']
        descriptions = ['The aging patriarch of an organized crime dynasty transfers control of his clandestine empire \n to his reluctant son.','A seventeen-year-old aristocrat falls in love with a kind but poor artist','Shallow, rich and socially successful Cher is at the top of her Beverly Hills high school s pecking scale. ','A priest with a haunted past and a novice on the threshold of her final vows are sent by the \n Vatican to investigate the death of a young nun in Romania \n and confront a malevolent force in the form of a demonic nun.','The presidencies of Kennedy and Johnson and other historical events unfold through the perspective of an \n Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.','After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets \n off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.','Following the death of publishing tycoon Charles Foster Kane, reporters scramble to uncover \n the meaning of his final utterance; Rosebud.','Atticus Finch, a lawyer in the Depression-era South, defends a black man against an undeserved \n rape charge, and his children against prejudice.','As a new threat to the galaxy rises, Rey, a desert scavenger, and Finn, an ex-stormtrooper, must join Han Solo \n and Chewbacca to search for the one hope of restoring peace.','Former cop Brian O Conner is called upon to bust a dangerous criminal and he recruits the \n help of a former childhood friend and street racer.']
        genres = ['comedy','romance','action','SF','horror','thriller','drama','adventure','crime','historical']
        for i in range(10):
            id = i+1
            title = choice(titles)
            description = choice(descriptions)
            genre = choice(genres)
            movie_list.append(Movie(str(id),title,description,genre))
        return movie_list

def initialize_rental_list(rental_list,rented_movies,movie_repo):
    years = [2020, 2021]
    movie_ids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    for i in range(5):
        id = i + 1
        id_client = randint(1, 10)
        id_movie = choice(movie_ids)
        movie_ids.remove(id_movie)
        d1 = randint(1, 17)
        m1 = randint(1, 11)
        y1 = 2020
        rented_d = date(y1, m1, d1)
        d2 = randint(1, 28)
        m2 = randint(1, 12)
        y2 = choice(years)
        due_d = date(y2, m2, d2)
        while rented_d >= due_d:
            d2 = randint(1, 28)
            m2 = randint(1, 12)
            y2 = choice(years)
            due_d = date(y2, m2, d2)

        rental = Rental(str(id), str(id_movie), str(id_client), rented_d, due_d)
        rental_list.append(rental)
        for m in movie_repo:
            if m.movie_id == rental.movie_id:
                rented_movies.append(m)
                movie_repo.remove_movie(m)
    return rental_list, rented_movies, movie_repo

undo_service = UndoService()
client_list = Iterable()
movie_list = []
rental_list = []
rented_movies = []
client_validator = ClientValidator()
movie_validator = MovieValidator()
rental_validator = RentalValidator()
settings = Settings()





if settings.typeofrepo == 'inmemory':
    client_repo = ClientRepository(initialize_client_list(client_list))
    client_service = ClientFunctionalities(client_repo, client_validator, undo_service)
    movie_repo = MovieRepository(initialize_movie_list(movie_list))
    movie_service = MovieFunctionalities(movie_repo, movie_validator, undo_service)
    rental_list, rented_movies, movie_repo = initialize_rental_list(rental_list, rented_movies, movie_repo)
    rental_repo = RentalRepository(rental_list, rented_movies)
    rental_service = RentalService(rental_repo, movie_repo, client_repo, rental_validator, undo_service, rented_movies)

elif settings.typeofrepo == 'text file':
    client_repo = ClientTextFileRepository(settings.client_repo)
    client_service = ClientFunctionalities(client_repo, client_validator, undo_service)
    movie_repo = MovieTextFileRepository(settings.movie_repo)
    movie_service = MovieFunctionalities(movie_repo, movie_validator, undo_service)
    rental_repo = RentalTextFileRepository(settings.rental_repo,rented_movies)
    rental_service = RentalService(rental_repo, movie_repo, client_repo, rental_validator, undo_service, rented_movies)

else: # if settings.typeofrepo == 'binary file':
    client_repo = ClientPickleRepository(settings.client_repo)
    client_service = ClientFunctionalities(client_repo, client_validator, undo_service)
    movie_repo = MoviePickleRepository(settings.movie_repo)
    movie_service = MovieFunctionalities(movie_repo, movie_validator, undo_service)
    rental_repo = RentalPickleRepository(settings.rental_repo,rented_movies)
    rental_service = RentalService(rental_repo, movie_repo, client_repo, rental_validator, undo_service, rented_movies)



ui = UI(client_service,movie_service,rental_service,undo_service)
ui.start()

