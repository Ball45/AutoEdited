import speech_recognition as sr
r = sr.Recognizer()
with sr.AudioFile("media/testb.wav") as source:
    audio = r.record(source)

try:
    instruction = r.recognize_google(audio, language="zh-TW", show_all=True)
    #instruction=r.recognize_google(audio_data=audio, key=None, language="zh-TW")
    print("Text: ",instruction)
    
    if "剪接" in instruction :
        print("剪接")
    else :
        print('pass')
#except Exception as e:
 #   print("Exception: "+str(e))

except r.UnknowValueError:
        Text = "無法翻譯"
except sr.RequestError as e:
        Text = "無法翻譯{0}".format(e)