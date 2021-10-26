from domain.client import Client, ClientValidator, ClientException
from repository.clientRepo import ClientRepository
from service.clientFunct import ClientFunctionalities
from domain.movie import Movie, MovieValidator, MovieException
from repository.movieRepo import MovieRepository
from service.movieFunct import MovieFunctionalities
import unittest
from iterable import Iterable, filter, combSort
from service.undoService import UndoService


class TestRepos(unittest.TestCase):
    def setUp(self):
        client_list = []
        self._client_repo = ClientRepository(client_list)
        self._client_repo.initialize_client_list()
        movie_list = []
        self._movie_repo = MovieRepository(movie_list)
        self._movie_repo.initialize_movie_list()

    def test_client_repo(self):
        self.assertEqual(len(self._client_repo),10)
        c = 'not a client'
        self.assertRaises(TypeError, self._client_repo.add_client,c)

    def test_movie_repo(self):
        self.assertEqual(len(self._movie_repo),10)
        m = 123
        self.assertRaises(TypeError, self._movie_repo.add_movie,m)



class TestServices(unittest.TestCase):
    def setUp(self):
        client_list = []
        client_repo = ClientRepository(client_list)
        client_repo.initialize_client_list()
        client_validator = ClientValidator()
        movie_list = []
        movie_repo = MovieRepository(movie_list)
        movie_repo.initialize_movie_list()
        movie_validator = MovieValidator()
        undo_service = UndoService()
        self._client_service = ClientFunctionalities(client_repo,client_validator,undo_service)
        self._movie_service = MovieFunctionalities(movie_repo,movie_validator,undo_service)


    def test_add_client(self):
        l = len(self._client_service.client_repo)
        c = Client('100','Ana')
        self._client_service.add_client(c)
        self.assertEqual(l+1,len(self._client_service.client_repo))
        self.assertEqual('100',self._client_service.client_repo[l].client_id)
        self.assertEqual('Ana', self._client_service.client_repo[l].name)
        self.assertRaises(ValueError,self._client_service.add_client,c)

    def test_remove_client(self):

        l = len(self._client_service.client_repo)
        self._client_service.remove_client('3')
        self.assertEqual(l-1,len(self._client_service.client_repo))
        self.assertRaises(ValueError,self._client_service.remove_client,'3')

    def test_update_client(self):

        self._client_service.update_client('1','id','999')
        self.assertEqual('999',self._client_service.client_repo[0].client_id)
        self._client_service.update_client('2','name','abcd')
        self.assertEqual('abcd',self._client_service.client_repo[1].name)
        self.assertRaises(ValueError,self._client_service.update_client,'5','sgsd','dfgdd')

    def test_add_movie(self):
        l = len(self._movie_service.movie_repo)
        m = Movie('100', 'Title','description','genre')
        self._movie_service.add_movie(m)
        self.assertEqual(l + 1, len(self._movie_service.movie_repo))
        self.assertEqual('100', self._movie_service.movie_repo[l].movie_id)
        self.assertEqual('Title', self._movie_service.movie_repo[l].title)
        self.assertEqual('description', self._movie_service.movie_repo[l].description)
        self.assertEqual('genre', self._movie_service.movie_repo[l].genre)
        self.assertRaises(ValueError, self._movie_service.add_movie, m)

    def test_remove_movie(self):
        l = len(self._movie_service.movie_repo)
        self._movie_service.remove_movie('3')
        self.assertEqual(l - 1, len(self._movie_service.movie_repo))
        self.assertRaises(ValueError, self._movie_service.remove_movie, '3')

    def test_update_movie(self):
        self._movie_service.update_movie('1', 'id', '999')
        self.assertEqual('999', self._movie_service.movie_repo[0].movie_id)
        self._movie_service.update_movie('2', 'title', 'abcd')
        self.assertEqual('abcd', self._movie_service.movie_repo[1].title)
        self.assertRaises(ValueError, self._movie_service.update_movie, '5', 'sgsd', 'dfgdd')



class TestEntities(unittest.TestCase):
    def test_client(self):
        c = Client('999','Mircea')
        self.assertEqual('999',c.client_id)
        self.assertEqual('Mircea',c.name)

    def test_movie(self):
        m = Movie('999','The nun','description','comedy')
        self.assertEqual('999',m.movie_id)
        self.assertEqual('The nun',m.title)
        self.assertEqual('description',m.description)
        self.assertEqual('comedy',m.genre)

class TestValidators(unittest.TestCase):
    def setUp(self):
        self._client_validator = ClientValidator()
        self._movie_validator = MovieValidator()

    def test_client_validator(self):
        c = Client('12g', 'A123')
        self.assertRaises(ClientException,self._client_validator.validate,c)

    def test_movie_validator(self):
        m = Movie('12d', 'a', 'asd', 'genre')
        self.assertRaises(MovieException,self._movie_validator.validate,m)


class TestIterable(unittest.TestCase):
    def setUp(self):
        self._iter = Iterable()
        self._iter.append('Alex')
        self._iter.append('Diana')
        self._iter.append('Radu')
        self._iter.append('Mirela')
        self._iter.append('Ana')

    def test_iterable(self):
        self.assertEqual(5,len(self._iter))

        self.assertEqual(self._iter[0],'Alex')
        self.assertEqual(self._iter[1], 'Diana')
        self.assertEqual(self._iter[2], 'Radu')
        self.assertEqual(self._iter[3], 'Mirela')
        self.assertEqual(self._iter[4], 'Ana')



        self._iter.__delitem__(self._iter[0])
        self._iter.__delitem__(self._iter[0])
        self.assertEqual(3,len(self._iter))

        self._iter.append('Alex')
        self.assertEqual(4, len(self._iter))

        for client in self._iter:
            self.assertIn(client,['Alex','Mirela','Radu','Ana'])

    def test_sort(self):
        combSort(self._iter, lambda str1,str2: str1 > str2)

        self.assertEqual(self._iter[0], 'Alex')
        self.assertEqual(self._iter[1], 'Ana')
        self.assertEqual(self._iter[2], 'Diana')
        self.assertEqual(self._iter[3], 'Mirela')
        self.assertEqual(self._iter[4], 'Radu')

    def test_filter(self):
        filtered_list = filter(self._iter, lambda str1: 'A' in str1)

        self.assertEqual(filtered_list[0], 'Alex')
        self.assertEqual(filtered_list[1], 'Ana')

        filtered_list_2 = filter(self._iter, lambda str1: 'na' in str1)

        self.assertEqual(filtered_list_2[0], 'Diana')
        self.assertEqual(filtered_list_2[1], 'Ana')