from domain.client import Client
from random import choice
from iterable import Iterable

class ClientRepository:

    def __init__(self, client_list:Iterable):
        self._client_list = client_list[:]

    @property
    def client_list(self):
        return self._client_list

    def get(self,item_name):
        return self._client_list[item_name]

    def add_client(self,client):

        if not isinstance(client, Client):
            raise TypeError('This is not a client!')
        self._client_list.append(client)

    def remove_client(self,client):
        x=0
        if not isinstance(client, Client):
            raise TypeError('This is not a client!')
        for i in range(len(self._client_list)):
            if self._client_list[i] == client:
                x = i

        self._client_list.__delitem__(x)

    def update_id_client(self,id,new):
        for i in range(len(self._client_list)):
            if self._client_list[i].client_id == id:
                self._client_list[i].client_id = new

    def update_name_client(self,id,new):
        for i in range(len(self._client_list)):
            if self._client_list[i].client_id == id:
                self._client_list[i].name = new

    def search_by_id(self,id):
        for c in self._client_list:
            if c.client_id == id:
                return c
        return None


    def __getitem__(self, key):
        return self._client_list[key]

    def __len__(self):
        return len(self._client_list)

    def initialize_client_list(self):
        first_name = ['Emilia', 'Alex', 'Andreea', 'Mihai', 'Petru', 'Costel', 'Geanina', 'Diana', 'Mirel', 'Gheorghe']
        last_name = ['Pop', 'Popescu', 'Gireada', 'Apostoliu', 'Iftime', 'Zlampa', 'Ionescu', 'Barbu', 'Vladimirescu',
                     'Visinescu']
        for i in range(10):
            id = i + 1
            first = choice(first_name)
            last = choice(last_name)
            name = first + ' ' + last
            self._client_list.append(Client(str(id), name))

