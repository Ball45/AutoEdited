# 0415--Install SpeechRecognition and try out

## TO DO LIST
- [ ] Learn SpeechRecognition
- [ ] Video => Audio (MoviePy, FFMPEG)
- [ ] How to dectect silence of voice file: get time interval of instruction
- [ ] instruction => text => command
- [ ] overlap comparison => Join time point
- [ ] video joint

## Install SpeechRecognition
- Install [pyaudio](https://anaconda.org/anaconda/pyaudio)
- SpeechRecognition example [p05.py](https://github.com/Uberi/speech_recognition/tree/master/examples)

```python
import speech_recognition as sr
# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)


# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
 ```

- Chinese SpeechRecognition [p04.py](https://markjong001.pixnet.net/blog/post/246140004)

```python
import speech_recognition


def Voice_To_Text():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
     # 介紹一下 with XXX as XX 這個指令
     # XXX 是一個函數或動作 然後我們把他 的output 放在 XX 裡
     # with 是在設定一個範圍 讓本來的 source 不會一直進行
     # 簡單的應用，可以參考
     # https://blog.gtwang.org/programming/python-with-context-manager-tutorial/
        print("請開始說話:")                               # print 一個提示 提醒你可以講話了
        r.adjust_for_ambient_noise(source)     # 函數調整麥克風的噪音:
        audio = r.listen(source)
     # with 的功能結束 source 會不見
     # 接下來我們只會用到 audio 的結果
    try:
        Text = r.recognize_google(audio, language="zh-TW")
        # 將剛說的話轉成  zh-TW 繁體中文 的 字串
        # recognize_google 指得是使用 google 的api
        # 也就是用google 網站看到的語音辨識啦~~
        # 雖然有其他選擇  但人家是大公司哩 當然優先用他的囉
    except r.UnknowValueError:
        Text = "無法翻譯"
    except sr.RequestError as e:
        Text = "無法翻譯{0}".format(e)
        # 兩個 except 是當語音辨識不出來的時候 防呆用的

    return Text
# fun定義結束


# 讓我們實際利用看看吧~
while True:
    Text = Voice_To_Text()
    print(Text)
```
