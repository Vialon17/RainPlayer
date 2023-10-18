import os, yaml, json, pickle
from typing import Literal, Generator

def get_father(file_name: str) -> str:
    return os.path.basename(os.path.dirname(file_name))

def get_sub_folder(os_path: str):
    if not os.path.isdir(os_path):
        raise ValueError(f"Invalid Path -> {os_path}")
    return [f.path for f in os.scandir(os_path) if f.is_dir()]

def file_generator(os_path: str, filter_suffix: list = None) -> Generator:
    if not os.path.isabs(os_path):
        os_path = os.path.join(os.getcwd(), os_path)
    for root, _, file_list in os.walk(os_path):
        for file in file_list:
            if os.path.splitext(file)[1].lstrip(".") not in filter_suffix:
                yield os.path.join(root, file)

class Config:

    support_config = ('json', 'yaml', 'pkl')

    def __init__(self, file_path: str):
        '''
        Create configure object
        e.g:
            path: -> 'C:/user/xxx/appdata/local/your_filename.txt'

            name -> 'your_filename.txt'

        '''
        self._file_path = os.path.join(os.getcwd(), file_path) if not os.path.isabs(file_path) else file_path
        self._file_name = os.path.basename(self._file_path)
        self._suffix_name = os.path.splitext(self._file_name)[1].replace('.', '')
        if self._suffix_name not in self.support_config:
            raise ValueError("Unsupported Configuration.")
        match self._suffix_name:
            case 'json':
                self._content = self.read_json(self._file_path)
            case 'yaml':
                self._content = self.read_yaml(self._file_path)
            case 'pkl':
                self._content = self.read_pkl(self._file_path)
        for key, value in self._content.items():
            setattr(Config, key, value)

    def transform(self, 
                  target_format: Literal['pkl', 'json', 'yaml'], mode: Literal['w', 'wb'] = 'w',
                  encoding: str = 'utf-8') -> str:
        '''
        Convert the file format to specified format
        '''
        if target_format not in self.support_config:
            raise ValueError("Unsupported file format!")
        with open(f'{self._file_name}.{target_format}', mode = mode, encoding = encoding) as fi:
            match target_format:
                case 'pkl':
                    pickle.dump(self._content, fi)
                case 'json':
                    json.dump(self._content, fi)
                case 'yaml':
                    yaml.dump(self._content, fi, indent = 4)
        return f'{self._file_name}.{target_format}'

    @staticmethod
    def read_pkl(file_name: str) -> object:
        if os.path.splitext(file_name)[-1] != '.pkl':
            raise ValueError("the file isn't a pickle file.")
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
        return data
    
    @staticmethod
    def write_pkl(obj: object, file_name: str) -> None:
        if os.path.splitext(file_name)[-1] != '.pkl':
            raise ValueError("the file isn't a pickle file.")
        with open(file_name, 'wb') as f:
            pickle.dump(obj, f)

    @staticmethod
    def read_yaml(file_name: str, encoding = "utf-8") -> dict:
        with open(file_name, "r", encoding = encoding) as f:
            data = yaml.load(f, Loader = yaml.FullLoader)
        return data

    @staticmethod
    def write_yaml(obj: object, file_name: str, encoding = "utf-8") -> None:
        with open(file_name, "w", encoding = encoding) as f:
            yaml.dump(obj, f, indent = 4)

    @staticmethod
    def read_json(file_name: str, encoding = "utf-8") -> dict:
        with open(file_name, "r", encoding = encoding) as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def write_json(obj: object, file_name: str, encoding = "utf-8") -> None:
        with open(file_name, "w", encoding = encoding) as f:
            json.dump(obj, f, ensure_ascii = False)