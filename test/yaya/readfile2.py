import speech_recognition as sr
r = sr.Recognizer()
with sr.AudioFile("media\\test1.wav") as source:
    audio = r.record(source)

try:
    s = r.recognize_google(audio_data=audio, key=None,
                           language="zh-TW", show_all=True)  # , show_all=True
    # print(str(s))
    print("Instruction: ")
    if "剪接" in str(s):
        print("剪接")
    else:
        print('pass')
# except Exception as e:
#     print("Exception: "+str(e))
except r.UnknowValueError:
    Text = "無法翻譯"
except sr.Requesterror as e:
    Text = "無法翻譯{0}".format(e)
