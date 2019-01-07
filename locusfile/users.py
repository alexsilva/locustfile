import json
import random


class User(object):
    """Parser and getter users"""
    def __init__(self, filepath):
        with open(filepath, 'rb') as jfile:
            data = jfile.read()
            self.data = json.loads(data)
        self.index = 0

    def get(self):
        """return a new user"""
        try:
            obj = self.data[self.index]
        except IndexError:
            self.index = 0
            obj = self.data[self.index]
        return obj

    def random(self):
        """Choose a random user"""
        return random.choice(self.data)