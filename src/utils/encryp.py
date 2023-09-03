from base64 import b64encode, b64decode
from cryptography.fernet import Fernet
import pickle
import os
from time import time

def to_pkl(obj: object, file_name: str) -> None:
    if os.path.splitext(file_name)[-1] != '.pkl':
        raise ValueError("the file isn't a pickle file.")
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)

def from_pkl(file_name: str) -> object:
    if os.path.splitext(file_name)[-1] != '.pkl':
        raise ValueError("the file isn't a pickle file.")
    with open(file_name, 'rb') as f:
        return pickle.load(f)



class Hasher: 

    _hash_table = {
        'base64': (b64encode, b64decode),
        'AES': ()
    }

    def __init__(self, hash: str = 'base64'):
        self._hash = hash

    def _create_aes_key() -> str:
        aes_key = Fernet.generate_key()
        to_pkl(aes_key, "cache/aes_key.pkl")
        return aes_key

    def encode(self, data: str) -> str:
        if not isinstance(data, str):
            raise TypeError("Need string type.")
        data = data.encode('utf-8')
        def aes():
            if not os.path.exists("cache/aes_key.pkl"):
                aes_key = self._create_aes_key()
            else:
                # check file info
                file_stat = os.stat("cache/aes_key.pkl")
                if file_stat.st_ctime != file_stat.st_mtime or time() - file_stat.st_ctime:
                    aes_key = self._create_aes_key()
        aes()

if __name__ == '__main__':
    ha = Hasher()
    ha.encode("https://asuq.com/asd?pass=134a2@ad&login=adi12a_aeq")