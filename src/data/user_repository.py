import json
from os import path


class UserRepository:
    __slots__ = '_data', '_users'

    def __init__(self):
        self._data = []
        self._users = {}

        base_dir = path.abspath(path.dirname(__file__))
        with open(path.join(base_dir, 'source', 'users.json')) as f:
            self._data = json.loads(f.read())
        for val in self._data:
            temp_key = val.get('username')
            self._users[temp_key] = val


    def get_all(self):
        return self._users

    def get_by_username(self, username):
        try:
            return self._users[username]
        except KeyError:
            return None

    def get_by_email(self, email):
        users = {}
        try:
            for val in self._data:
                temp_key = val.get('email')
                users[temp_key] = val
            return users[email]
        except KeyError:
            return None

    def get_by_id(self, id):
        try:
            for username, user in self._users.items():
                if user['id'] == id:
                    return user
        except KeyError:
            return None
