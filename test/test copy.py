from src.utils import Hasher, Config
from src.song.tidy import walk_songs, parse_song, Song_Lib, parse_single_folder
from src.utils.config import file_generator, get_sub_folder

song_suffix = ('mp3', 'flac', 'wav', 'ape', 'ogg')
lib = Song_Lib(r'E:\Songs')
lib.pure.to_excel('temp.xlsx')