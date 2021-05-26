import speech_recognition as sr
r = sr.Recognizer()
with sr.AudioFile("media\\test1.wav") as source:
    audio = r.record(source)

try:
    s = r.recognize_google(audio_data=audio, key=None,
                           language="zh-TW", show_all=True)
    print("Text: "+s)
    if '剪接' in s:
        print("剪接")
    else:
        print('pass')
except Exception as e:
    print("Exception: "+str(e))
