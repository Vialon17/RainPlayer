from base64 import b64encode, b64decode
from cryptography.fernet import Fernet
from typing import Literal
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

    _fernet_key_path = "cache/fernet_key.pkl"

    def __init__(self, hash: str = 'base64'):
        self._hash = hash

    def _create_fernet_key(self) -> str:
        fernet_key = Fernet.generate_key()
        to_pkl(fernet_key, self._fernet_key_path)
        print(fernet_key)
        return fernet_key

    def _get_key(self) -> str:
        if os.path.exists(self._fernet_key_path):
            file_stat = os.stat(self._fernet_key_path)
            fernet_key = from_pkl(self._fernet_key_path)
            print(file_stat.st_ctime, file_stat.st_mtime)
            if file_stat.st_ctime == file_stat.st_mtime and isinstance(fernet_key, str):
                return fernet_key
        # return self._create_fernet_key()
         
    
    def encode(self, data: str) -> str:
        if not isinstance(data, str):
            raise TypeError("Need string type.")
        data = data.encode('utf-8')

    def fernet(self, data: str , method: Literal['encode', 'decode']):
        if method not in ('encode', 'decode'):
            raise ValueError("Invalid method.")
        key = self._get_key()
        cipher_suite = Fernet(key)
        if method == 'encode':
            # encrypted data
            re_data = cipher_suite.encrypt(data.encode())
        else:
            # decrypted data
            re_data = cipher_suite.decrypt(data).decode()
        return re_data

if __name__ == '__main__':
    ha = Hasher()
    print(ha.fernet(b'gAAAAABk9fMkDreW8T_aoj9L1eH9OR_noXpqzTYtGruBYt_nmaee1yiE0IK2i9grLCj3qAecfhAIwttH-myaBz-hleWh-SW6Vw==', 'decode'))