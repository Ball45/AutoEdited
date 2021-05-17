import speech_recognition as sr
r = sr.Recognizer()
with sr.AudioFile("media/testa.wav") as source:
    audio = r.record(source)

try:
    s = r.recognize_google(audio, language="zh-TW")
    print("Text: "+s)
    if '剪接' in s :
        print("剪接")
    else :
        print('pass')
except Exception as e:
    print("Exception: "+str(e))

