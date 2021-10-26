from domain.client import Client, ClientValidator, ClientException, ClientValidationException
from repository.clientRepo import ClientRepository
from service.undoService import FunctionCall, Operation
from iterable import filter

class ClientFunctionalities:

    def __init__(self,client_repo:ClientRepository, client_validator:ClientValidator, undo_service):
        self._repo = client_repo
        self._validator = client_validator
        self._undo_service = undo_service

    @property
    def client_repo(self):
        return self._repo.client_list

    @property
    def client_validator(self):
        return self._validator



    def add_client(self,client):
        for c in self._repo:
            if c.client_id == client.client_id :
                raise ValueError('Duplicate id!')
        try:
            self.client_validator.validate(client)
            self._repo.add_client(client)
            undo_op = FunctionCall(self._repo.remove_client, client)
            redo_op = FunctionCall(self._repo.add_client,client)
            op = Operation(undo_op,redo_op)
            self._undo_service.record(op)

        except ClientValidationException as cve:
           print(str(cve))



    def remove_client(self,id_client):
        found = False
        for c in self._repo:
            if c.client_id == id_client:
                found = True
                client = self._repo.search_by_id(id_client)
                self._repo.remove_client(c)
                undo_op = FunctionCall(self._repo.add_client,client)
                redo_op = FunctionCall(self._repo.remove_client,client)
                op = Operation(undo_op,redo_op)
                self._undo_service.record(op)

        if not found:
            raise ValueError('Client with given ID does not exist!')

    def update_client(self,id,key,new):
        found = False
        for c in self._repo:
            if c.client_id == id:
                found = True
                client = self._repo.search_by_id(id)
                init_name = client.name
                init_id = client.client_id
                if key == 'name':
                    self._repo.update_name_client(id, new)
                    undo_op = FunctionCall(self._repo.update_name_client,id,init_name)
                    redo_op = FunctionCall(self._repo.update_name_client,id,new)
                    op = Operation(undo_op,redo_op)
                    self._undo_service.record(op)
                elif key == 'id':
                    self._repo.update_id_client(id, new)
                    undo_op = FunctionCall(self._repo.update_id_client, id, init_id)
                    redo_op = FunctionCall(self._repo.update_name_client, id, new)
                    op = Operation(undo_op, redo_op)
                    self._undo_service.record(op)


                else:
                    raise ValueError('You can only update the name or the id! ')
        if not found:
            raise ValueError('Client with given ID does not exist!')


    def search_client(self,key,word):
        result = []
        if key == 'id':
            result = filter(self.client_repo, lambda c : word in c.client_id)
        elif key == 'name':
            result = filter(self.client_repo, lambda c: word in c.name)
        else:
            raise ValueError('You can only search clients using id or name!')

        return result



