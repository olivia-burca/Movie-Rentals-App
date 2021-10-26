from domain.client import Client
from repository.clientRepo import ClientRepository


class ClientTextFileRepository(ClientRepository):


    def __init__(self, file_name='clients.txt'):
        super().__init__([])
        self._file_name = file_name
        self._load()

    def add_client(self,client):
        super().add_client(client)
        self._save()

    def remove_client(self,client):
        super().remove_client(client)
        self._save()

    def update_id_client(self, id, new):
        super().update_id_client(id, new)
        self._save()

    def update_name_client(self, id, new):
        super().update_name_client(id, new)
        self._save()

    def _save(self):
        f = open(self._file_name, 'wt')
        for client in self._client_list:
            line = str(client.client_id) + ';' + client.name
            f.write(line)
            f.write('\n')
        f.close()

    def _load(self):

        f = open(self._file_name, 'rt')  # read text
        lines = f.readlines()
        f.close()

        for line in lines:

            line = line.strip().split(';')
            super().add_client(Client(line[0], line[1]))