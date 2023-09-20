from src.utils import Hasher, from_pkl
from src.tidy import File

f = File("test/songs/NOVA - DELA.mp3", easy = True)
print(f.tags)