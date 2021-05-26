import speech_recognition as sr


# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)


# recognize speech using Google Speech Recognition
try:
   text = r.recognize_google(audio, language='en-IN', show_all=True)
   print(text)
   # print("Google Speech Recognition thinks you said " + recognize_google(audio_data=audio, key=None, language="zh-TW", show_all=True))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
