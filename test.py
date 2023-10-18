from src.utils import Hasher, Config
from src.tidy import walk_songs, parse_song, Song_Lib
# mp3, flac, wav, ape, ogg
# df1 = Song_Lib("E:\Songs")
# print(df1._lib)

conf = Config('config/config.yaml')
conf.transform('json')