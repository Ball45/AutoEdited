# 0512--[Instruction Recognition](https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python)

# Try out
```python
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.AudioFile("media/testa.wav") as source:
        audio = r.record(source)

    try:
        command = ['剪接', '重複']
        s = r.recognize_google(audio, language="zh-TW")
        print("Text: "+s)
        if '剪接' in s :
            print("剪接")
        else :
            print('pass')
    except Exception as e:
        print("Exception: "+str(e))
```
### OUTPUT
```
Text:  這是專輯的聲音音檔剪接軟體的測試音檔
剪接
```
