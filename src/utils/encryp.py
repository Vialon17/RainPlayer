from base64 import b64encode, b64decode
from cryptography.fernet import Fernet
import pickle
import os

def to_pkl(obj: object, file_name: str) -> None:
    if os.path.splitext(file_name) != '.pkl':
        raise ValueError("the file isn't a pickle file.")
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)

def from_pkl(file_name: str) -> object:
    if os.path.splitext(file_name) != '.pkl':
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

    def encode(self, data: str) -> str:
        if not isinstance(data, str):
            raise TypeError("Need string type.")
        data = data.encode('utf-8')
        def aes():
            aes_key = Fernet.generate_key()

if __name__ == '__main__':
    ha = Hasher()
    ha.encode("https://asuq.com/asd?pass=134a2@ad&login=adi12a_aeq")