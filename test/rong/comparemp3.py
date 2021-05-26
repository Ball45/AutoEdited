
from compare_mp3 import compare

songmp31 = "media/testa.mp3"
songmp32 = "media/testb.mp3"

if compare(songmp31, songmp32):
    print('Files contain the same audio')

