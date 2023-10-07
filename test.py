from src.utils import Hasher
from src.tidy import walk_songs, parse_song

# mp3, flac, wav, ape, ogg
df1 = walk_songs("E:\Songs\十七韵倾城喜欢的音乐")
print(df1)