import base64
import pickle

class Hasher:

    _hash_table = {
        'base64'
    }
    def __init__(self, hash: str = 'base64'):
        self._hash = hash

    def encode(self, value: str) -> str:
        pass