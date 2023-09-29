import os, pickle, yaml, json
from traceback import print_exc
from typing import Literal


def get_father(file_name: str) -> str:
    return os.path.basename(os.path.dirname(file_name))

class Configuration:

    support_config = ('json', 'yaml', 'pkl')

    def __init__(self, file_name: str):
        if not os.path.isabs(file_name):
            self._path = os.path.join(os.getcwd(), file_name)
        else:
            self._path = file_name
        if not os.path.isfilel(self._path):
            raise ValueError("Invalid File Path.")
        self._name = os.path.basename(self._path)
        self._suffix_name = os.path.splitext(self._name)[1]
        if self._suffix_name not in self.support_config:
            raise ValueError("Unsupported Configuration.")

    def write(self, 
              target: object | str, 
              mode = Literal['w', 'w+', 'wb', 'wb+'], 
              encoding = "utf-8") -> bool:
        try:
            with open(self._path, mode = mode, encoding = encoding) as fi:
                match self._suffix_name:
                    case 'json':
                        json.dump(target, fi, ensure_ascii = False)
                    case 'yaml':
                        yaml.dump(target, fi, indent = 4)
                    case 'pkl':
                        pickle.dump(target, fi)
            return True
        except:
            print_exc(); return False
    
    def read(self,
             mode = Literal['r', 'r+', 'rb', 'rb+'],
             encoding = "utf-8") -> dict | object:
        with open(self._path, mode = mode, encoding = encoding) as fi:
            match self._suffix_name:
                case 'json':
                    re_target = json.load(fi)
                case 'yaml':
                    re_target = yaml.load(fi, Loader = yaml.FullLoader)
                case 'pkl':
                    re_target = pickle.load(fi, encoding = encoding)
        return re_target

    def transform(self, target_format: Literal['pkl', 'json', 'yaml']):
        pass


def write_pkl(obj: object, file_name: str) -> None:
    if os.path.splitext(file_name)[-1] != '.pkl':
        raise ValueError("the file isn't a pickle file.")
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)

def read_pkl(file_name: str) -> object:
    if os.path.splitext(file_name)[-1] != '.pkl':
        raise ValueError("the file isn't a pickle file.")
    with open(file_name, 'rb') as f:
        return pickle.load(f)

