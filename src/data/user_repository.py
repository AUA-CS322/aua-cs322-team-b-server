import json
import os


class UserRepository:
    def __init__(self):
        self._data = []
        self._users = {}

        with open(os.path.join(os.getcwd(), 'data', 'source', 'users.json')) as f:
            self._data = json.loads(f.read())
        for val in self._data:
            temp_key = val.pop('username')
            self._users[temp_key] = val

    def get_all(self):
        return self._users

    def get_by_username(self, username):
        return self._users[username]
