class ClientException(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class ClientValidationException(ClientException):
    def __init__(self, error_list):
        self._errors = error_list

    def __str__(self):
        result = ''

        for er in self._errors:
            result += er
            result += '\n'
        return result


class ClientValidator:
    @staticmethod
    def _is_id_valid(id):
        valid = True
        for i in range(len(id)):
            if not id[i].isdigit():
                valid = False

        return valid

    @staticmethod
    def _is_name_valid(name):
        valid = True
        for i in range(len(name)):
            if name[i] != ' ':
                if not name[i].isalpha():
                    valid = False
        return valid

    def validate(self, client):
        errors = []
        # V1 - All properties are non-empty
        if not self._is_id_valid(client.client_id):
            errors.append('CLient ID should only contain digits!')
        if not self._is_name_valid(client.name):
            errors.append(('CLient name should only contain letters!'))
        if len(client.name) < 3:
            errors.append('Client name should have at least 3 letters!')


        if len(errors) > 0:
            raise ClientValidationException(errors)



class Client:

    def __init__(self,client_id,name):
        if not isinstance(client_id,str):
            raise ClientException('Invalid value for id!')
        if not isinstance(name,str):
            raise ClientException('Invalid name!')

        self._client_id = client_id
        self._name = name


    @property
    def client_id(self):
        return self._client_id

    @property
    def name(self):
        return self._name

    @client_id.setter
    def client_id(self,value):
        self._client_id = value

    @name.setter
    def name(self, value):
        self._name = value

    def __str__(self):
        return 'ID: ' + str(self._client_id) + ', name: ' + self._name