import speech_recognition as sr
r = sr.Recognizer()
with sr.AudioFile("media\\test1.wav") as source:
    audio = r.record(source)

try:
    s = r.recognize_google(audio, language="zh-TW")
    print("Text: "+s)
    if '9' in s:
        print("yes")
    # else:print("no")
except Exception as e:
    print("Exception: "+str(e))
