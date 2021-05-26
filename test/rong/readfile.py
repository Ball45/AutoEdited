import speech_recognition as sr
r = sr.Recognizer()
<<<<<<< HEAD
with sr.AudioFile("media\\test1.wav") as source:
    audio = r.record(source)

try:
    s = r.recognize_google(audio_data=audio, key=None,
                           language="zh-TW", show_all=True)
    print("Text: "+s)
    if '剪接' in s:
=======
with sr.AudioFile("media/testb.wav") as source:
    audio = r.record(source)

try:
    instruction = r.recognize_google(audio, language="zh-TW", show_all=True)
    #instruction=r.recognize_google(audio_data=audio, key=None, language="zh-TW")
    print("Text: ",instruction)
    
    if "剪接" in instruction :
>>>>>>> 63ac1d0d87e96201d588c63afa1ffcb841a22d8e
        print("剪接")
    else:
        print('pass')
<<<<<<< HEAD
except Exception as e:
    print("Exception: "+str(e))
=======
#except Exception as e:
 #   print("Exception: "+str(e))

except r.UnknowValueError:
        Text = "無法翻譯"
except sr.RequestError as e:
        Text = "無法翻譯{0}".format(e)
>>>>>>> 63ac1d0d87e96201d588c63afa1ffcb841a22d8e
