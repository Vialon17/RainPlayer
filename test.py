from src.utils import Hasher, from_pkl

ha = Hasher()
ha.encode("152zsq7123ad")
a = from_pkl("cache/aes_key.pkl")

'''
    os.stat_result(st_mode=33206, st_ino=1970324836979799, st_dev=1748711056, st_nlink=1, st_uid=0, st_gid=0, st_size=59, st_atime=1693732003, st_mtime=1693731901, st_ctime=1693731901)
'''