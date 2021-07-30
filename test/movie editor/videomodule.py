import os
import auditok
from pydub import AudioSegment
from moviepy.editor import *
from moviepy.editor import VideoFileClip
import numpy as np
import cv2 as cv
import speech_recognition as sr
import numpy as np

# mp4 轉成 wav -----------------------------
#mp4file = "media/tainanvlog.mp4"
wavfile = "media/testc.wav"
#os.system("ffmpeg -i "+mp4file+" "+wavfile)

# 測試靜音 ----------------------------------
record_start = np.zeros(1000)
record_end = np.zeros(1000)
duration = np.zeros(1000)
speech = np.zeros(1000)
num = 0

# split returns a generator of AudioRegion objects
sound = AudioSegment.from_file(wavfile, format="wav") 
audio_regions = auditok.split(
    wavfile,
    min_dur=0.2,        # minimum duration of a valid audio event in seconds
    max_dur=100,        # maximum duration of an event
    max_silence=2,      # maximum duration of tolerated continuous silence within an event
    energy_threshold=40  # threshold of detection
)

for i, r in enumerate(audio_regions):
    record_start[i] = r.meta.start
    record_end[i] = r.meta.end
    speech[i] = record_end[i] - record_start[i]
    print("Speech  {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i,r=r), "Duration : ", speech[i])
    num = num+1

for j in range(num-1):
    #evaluate silence section length
    duration[j] = record_start[j+1] - record_end[j]
    print("Silence ", j, " :", round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ', duration[j])

    #if there are two continuous silence sections >2.5 
    if duration[j-1] > 2.5 and duration[j] > 2.5 and speech[j] < 5.0:
        print("instruction : ", round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')
        a=int(record_start[j])
        b=int(record_end[j])+1
        print(a,b,type(a))
        instruction = sound[a*1000:b*1000]
        filename=instruction.export("media/instruction.wav",format="wav")
# 辨識是否為語音指令“剪接” ---------------------------
        r = sr.Recognizer()
        with sr.AudioFile("media/instruction.wav") as source:
            audio = r.record(source)

        try:
            s = r.recognize_google(audio_data=audio, key=None,language="zh-TW", show_all=True)  # , show_all=True
            print("Instruction: ")
            if "剪接" in str(s):
                print("剪接")
            else:
                print('pass')

        except r.UnknowValueError:
            Text = "無法翻譯"
        except sr.Requesterror as e:
            Text = "無法翻譯{0}".format(e)