import pickle

from repository.clientRepo import ClientRepository


class ClientPickleRepository(ClientRepository):

    def __init__(self,file_name):
        super().__init__([])
        self._file_name = file_name
        self._load()

    def _save(self):
        f = open(self._file_name,'wb')
        pickle.dump(self._client_list,f)
        f.close()

    def _load(self):
        result = []
        try:
            f = open(self._file_name,'rb')
            self._client_list = pickle.load(f)
            f.close()
            return self._client_list
        except EOFError:
            return result
        except IOError as e:
            raise e


    def add_client(self, client):
        super().add_client(client)
        self._save()

    def remove_client(self, client):
        super().remove_client(client)
        self._save()

    def update_id_client(self, id, new):
        super().update_id_client(id, new)
        self._save()

    def update_name_client(self, id, new):
        super().update_name_client(id, new)
        self._save()
