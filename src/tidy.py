from mutagen import File
import os

def get_song_info(file_name: str) -> tuple:
    '''
    return: ["title", "artist", "album", "size"]
    '''
    info_tuple = []
    song_info = File(file_name).tags
    for prop in ['title', 'artist', 'album']:
        info_tuple.append(song_info[prop]) if song_info.get(prop) is not None else info_tuple.append(None)
    info_tuple.append(os.stat(file_name).st_size)
    return tuple(info_tuple)

