from mutagen import File
from mutagen.apev2 import APEv2
import os, re
import pandas as pd

def get_pure_string(target: str):
    bracket_pattern = r"\([^)]*\)|\（[^)]*\）"
    return re.sub(bracket_pattern, '', target)

def parse_song(file_name: str, easy = True) -> dict:
        '''
        Parse song file, 
        '''
        if 'ape' in file_name:
            song_info = APEv2(file_name)
        else:
            song_info = File(file_name, easy = easy).tags
        info_dict = {
            'title': get_pure_string(song_info.get('title', [''])[0]),
            'artist': get_pure_string(song_info.get('artist', [''])[0]),
            'album': get_pure_string(song_info.get('album', [''])[0]),
            'size': os.stat(file_name).st_size
            }
        if '/' in info_dict['artist']:
            info_dict['artist'] = info_dict['artist'].split('/')
        else:
            info_dict['artist'] = [info_dict['artist']]
        return info_dict

def walk_songs(folder: str) -> pd.DataFrame:
    '''
    Walk the playlist folder, get all song's info
    '''
    song_suffix = ('mp3', 'flac', 'wav', 'ape', 'ogg')
    if not os.path.isdir(folder):
        raise ValueError("Invalid Folder Path!")
    re_list = {i:'' for i in os.listdir(folder) if os.path.isdir(os.path.join(folder, i))}
    damaged_list, re_list['damaged'] = [], []
    if len(re_list) == 1:
         song_list = []
         for root, _, file_list in os.walk(folder):
            for file in file_list:
                file_extension = os.path.splitext(file)[1].lstrip(".")
                if file_extension in song_suffix:
                    try:
                        song_info = parse_song(os.path.join(root, file))
                    except:
                        song_info = dict()
                    song_info["file_name"] = file
                    song_list.append(song_info) if 'title' in song_info and song_info['title'] != '' else damaged_list.append(file)
            re_list[os.path.basename(folder)] = pd.DataFrame(song_list)
            re_list['damaged'].extend(damaged_list)
    else:
        for dir in [i for i in re_list.keys() if i != 'damaged']:
            temp_list = walk_songs(os.path.join(folder, dir))
            re_list['damaged'].extend(temp_list['damaged'])
            del temp_list['damaged']; re_list.update(temp_list)
    return re_list
