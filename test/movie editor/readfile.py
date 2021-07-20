import speech_recognition as sr
import numpy as np

r = sr.Recognizer()
with sr.AudioFile("media/testc.wav") as source:
    audio = r.record(source)

instruction = np.zeros(100)
num = 0

try:
    instruction = r.recognize_google(audio, language="zh-TW", show_all=True)
    #instruction=r.recognize_google(audio_data=audio, key=None, language="zh-TW")
    #print("Text: ", instruction)

    flag = False
    for t in instruction['alternative']:
        print(t)
        if "剪接" in t['transcript']:
            flag = True
    if flag:
        print('剪接')
    else:
        print('pass')

    # if "剪接" in instruction:
     #   print("剪接")
    # else:
     #   print('pass')
# except Exception as e:
 #   print("Exception: "+str(e))
# except Exception as e:
 #   print("Exception: "+str(e))

except r.UnknowValueError as e:
    Text = "無法翻譯"
except sr.RequestError as e:
    Text = "無法翻譯{0}".format(e)
