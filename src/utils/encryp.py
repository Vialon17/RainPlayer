from cryptography.fernet import Fernet
from typing import Literal
from .files import write_pkl, read_pkl
import os, time

class Hasher:

    _fernet_key_path = "cache/fernet_key.pkl"

    def __init__(self, hash: str = 'base64'):
        self._hash = hash

    def _create_fernet_key(self) -> str:
        '''
            create fernet key with timestamp.
        '''
        fernet_key = Fernet.generate_key()
        now_time = time.time()
        write_pkl([fernet_key, now_time], self._fernet_key_path)
        return fernet_key

    def _get_key(self) -> str:
        '''
            get fernet key.
        '''
        if os.path.exists(self._fernet_key_path):
            fernet_key, creat_time = read_pkl(self._fernet_key_path)
            if isinstance(fernet_key, bytes) and time.time() - creat_time <= 5 * 86400:
                return fernet_key
        return self._create_fernet_key()

    def fernet(self, data: str , method: Literal['encode', 'decode']) -> str | bytes:
        '''
            Use AES Algorithm encrypt string.

            Attention: please keep the "cache/fernet_key.pkl" safe!
        '''
        if method not in ('encode', 'decode'):
            raise ValueError("Invalid method.")
        key = self._get_key()
        cipher_suite = Fernet(key)
        if method == 'encode':
            re_data = cipher_suite.encrypt(data.encode())
        else:
            re_data = cipher_suite.decrypt(data).decode()
        return re_data

if __name__ == '__main__':
    ha = Hasher()
    print(ha.fernet("ase1%3!2p0AYus", 'encode'))
    print(ha.fernet(b"gAAAAABk-ISV2bl3-zKGj6HLySWUWDahT96vGy96vvOPw-74xowT5AIl7i80GrHjwz5Ipg0xFSWLYlZGIhb6B5fPLJ0VQyiTcQ==", 'decode'))