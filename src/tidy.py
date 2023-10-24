from mutagen import File
from mutagen.apev2 import APEv2
import os
import pandas as pd
from typing import Literal, Iterable
from .utils.format import get_pure_string
from .utils.config import file_generator, get_sub_folder

def parse_song(file_name: str, easy: bool = True) -> dict:
        '''
        Parse song file
        '''
        song_info = APEv2(file_name) \
            if 'ape' in file_name else File(file_name, easy = easy).tags
        info_dict = {
            'title': get_pure_string(song_info.get('title', [''])[0]),
            'artist': get_pure_string(song_info.get('artist', [''])[0]),
            'album': get_pure_string(song_info.get('album', [''])[0]),
            'size': os.stat(file_name).st_size
            }
        info_dict['artist'] = info_dict['artist'].split('/') \
            if '/' in info_dict['artist'] else [info_dict['artist']]
        return info_dict
def parse_single_folder(target_path: str, fliter_suffix: list = None) -> tuple[pd.DataFrame, list]:
    '''
    Parse single songs folder
    '''
    damaged_list, song_list = [], []
    for file in file_generator(target_path, fliter_suffix):
        try:
            song_info = parse_song(os.path.join(target_path, file))
        except:
            song_info = dict()
        song_info["file_name"] = file
        song_list.append(song_info) if 'title' in song_info and song_info['title'] != '' \
            else damaged_list.append(file)
    return pd.DataFrame(song_list), damaged_list

def walk_songs(target_path: str, 
               fliter_folder: Iterable = None,
               song_suffix = ('mp3', 'flac', 'wav', 'ape', 'ogg')) -> pd.DataFrame:
    '''
    Walk the playlist folder, Get song's info

    Attention: the function will ignore the songs under the root folder path
    '''
    target_path = target_path if os.path.isabs(target_path) \
        else os.path.join(os.getcwd(), target_path)
    child_folders = get_sub_folder(target_path, fliter_folder)
    songs_dict = {}; songs_dict['damaged'] = []
    if child_folders == []:
        return {os.path.basename(child_folders[0]): parse_single_folder(child_folders[0], song_suffix)[0]}
    else:
        for dir in child_folders:
            sub_songs, sub_damage = parse_single_folder(dir, song_suffix)
            songs_dict['damaged'].extend(sub_damage)
            songs_dict.update({os.path.basename(dir): sub_songs})
    return songs_dict

class Song_Lib:
    # subclass of dataframe
    _columns = ('title', 'artist', 'album', 'size', 'file_name')

    def __init__(self, dataframe: pd.DataFrame | dict[str: pd.DataFrame] | str):
        match dataframe:
            case dataframe if isinstance(dataframe, dict):
                self._lib = pd.concat([dataframe[key] for key in dataframe if key != 'damaged'], axis = 1, ignore_index = True, sort = True)
            case dataframe if isinstance(dataframe, pd.DataFrame):
                self._lib = dataframe
            case dataframe if isinstance(dataframe, str):
                dataframe = walk_songs(dataframe)
                self._lib = pd.concat(
                    [dataframe[key] for key in dataframe if key != 'damaged'], axis = 0, ignore_index = True, sort = True)
            case _:
                raise ValueError("Invalid DataFrame")
        
    def __getattr__(self, attr_name: str):
        if hasattr(self._lib, attr_name):
            return getattr(self._lib, attr_name)
        raise AttributeError(f"Didn't find the attribute '{attr_name}'")
        
    @property
    def pure(self) -> pd.DataFrame:
        '''
        Return the unrepeated song library datafram
        '''
        self._pure: pd.DataFrame = self._lib.sort_values(by = ['title', 'size'], ignore_index = True)
        self._pure.drop_duplicates(subset = 'title', keep = 'first', inplace = True)
        return self._pure

    def find(self, name: str, mode: Literal['fuzzy', 'accurate'] = 'accurate') -> dict | str | None:
        from fuzzywuzzy import process
        if mode == 'accurate':
            if name not in self.pure['title']:
                return None
            return self.pure[name]
        elif mode == 'fuzzy':
            return {key: value for key, value in process.extract(name, self.pure['title'])}
    
    def add(self, add_one: pd.DataFrame | dict[str, pd.DataFrame]) -> None:
        if isinstance(add_one, pd.DataFrame):
            if set(self._columns) - set(add_one.columns) != set():
                raise ValueError("Incomplete Columns Info")
            pure_one = add_one[['title', 'artist', 'album', 'size', 'file_name']]
            self._lib = pd.concat([self._lib, pure_one], axis = 0, ignore_index = True, sort = True)
        elif isinstance(add_one, dict):
            for key in add_one:
                if set(self._columns) - set(add_one[key].columns) == set():
                    self._lib = pd.concat([self._lib, add_one[key][['title', 'artist', 'album', 'size', 'file_name']]],
                                          axis = 0, ignore_index = True, sort = True)
        raise ValueError('Unsupported Dataframe.')