from random import choice

from domain.movie import Movie
from iterable import Iterable

class MovieRepository:

    def __init__(self,movie_list:Iterable):
        self._movie_list = movie_list[:]

    @property
    def movie_list(self):
        return self._movie_list

    def get(self,item_name):
        return self._movie_list[item_name]

    def add_movie(self,movie):

        if not isinstance(movie, Movie):
            raise TypeError('This is not a movie!')
        self._movie_list.append(movie)

    def remove_movie(self,movie):
        x=0
        if not isinstance(movie, Movie):
            raise TypeError('This is not a movie!')
        for i in range(len(self._movie_list)):
            if self._movie_list[i] == movie:
                x = i

        self._movie_list.__delitem__(x)

    def update_id_movie(self,id,new):
        for i in range(len(self._movie_list)):
            if self._movie_list[i].movie_id == id:
                self._movie_list[i].movie_id = new

    def update_title_movie(self,id,new):
        for i in range(len(self._movie_list)):
            if self._movie_list[i].movie_id == id:
                self._movie_list[i].title = new

    def update_description_movie(self,id,new):
        for i in range(len(self._movie_list)):
            if self._movie_list[i].movie_id == id:
                self._movie_list[i].description = new

    def update_genre_movie(self,id,new):
        for i in range(len(self._movie_list)):
            if self._movie_list[i].movie_id == id:
                self._movie_list[i].genre = new

    def search_by_id(self,id):
        for m in self._movie_list:
            if m.movie_id == id:
                return m

    def __getitem__(self, key):
        return self._movie_list[key]

    def __len__(self):
        return len(self._movie_list)

    def initialize_movie_list(self):

        titles = ['The Godfather', 'The Nun', 'Citizen Kane', '2001: A Space Odyssey', 'Star Wars', 'Forrest Gump',
                  'To kill a mockingbird', 'Titanic', 'Clueless', 'Fast and Furious']
        descriptions = [
            'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire \n to his reluctant son.',
            'A seventeen-year-old aristocrat falls in love with a kind but poor artist',
            'Shallow, rich and socially successful Cher is at the top of her Beverly Hills high school s pecking scale. ',
            'A priest with a haunted past and a novice on the threshold of her final vows are sent by the \n Vatican to investigate the death of a young nun in Romania \n and confront a malevolent force in the form of a demonic nun.',
            'The presidencies of Kennedy and Johnson and other historical events unfold through the perspective of an \n Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.',
            'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets \n off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.',
            'Following the death of publishing tycoon Charles Foster Kane, reporters scramble to uncover \n the meaning of his final utterance; Rosebud.',
            'Atticus Finch, a lawyer in the Depression-era South, defends a black man against an undeserved \n rape charge, and his children against prejudice.',
            'As a new threat to the galaxy rises, Rey, a desert scavenger, and Finn, an ex-stormtrooper, must join Han Solo \n and Chewbacca to search for the one hope of restoring peace.',
            'Former cop Brian O Conner is called upon to bust a dangerous criminal and he recruits the \n help of a former childhood friend and street racer.']
        genres = ['comedy', 'romance', 'action', 'SF', 'horror', 'thriller', 'drama', 'adventure', 'crime',
                  'historical']
        for i in range(10):
            id = i + 1
            title = choice(titles)
            description = choice(descriptions)
            genre = choice(genres)
            self._movie_list.append(Movie(str(id), title, description, genre))