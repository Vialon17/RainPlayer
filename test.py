from src.utils import Hasher, from_pkl
from src.tidy import walk_songs, parse_song
# mp3, flac, wav, ape, ogg, 
df1 = walk_songs("E:\Songs")
print(df1)