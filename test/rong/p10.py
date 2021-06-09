
from pydub import AudioSegment

SECOND = 1000

sound = AudioSegment.from_wav("media/testc.wav")

sound = sound[24.75*SECOND:27.75*SECOND]

sound.export('media/cuttestc.mp3')

