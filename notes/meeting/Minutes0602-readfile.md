# 0526 -- update readfile
 
 ## Read file [參考](https://blog.csdn.net/ainivip/article/details/98040557)
- [x] 如果show all ,要如何測要”剪接“？
-  可以辨識全部選instruction alternative

```python
import speech_recognition as sr
import numpy as np

r = sr.Recognizer()
with sr.AudioFile("media/testa.wav") as source:
    audio = r.record(source)

try:
    instruction = r.recognize_google(audio, language="zh-TW", show_all=True)
   
    flag = False
    for t in instruction['alternative']:
        print(t)
        if "剪接" in t['transcript']:
            flag = True
    if flag:
        print('剪接')
    else:
        print('pass')

except r.UnknowValueError:
    Text = "無法翻譯"
except sr.RequestError as e:
    Text = "無法翻譯{0}".format(e)
```

## OUTPUT
```
{'transcript': '這是專輯的聲音音檔剪接軟體的測試音檔', 'confidence': 0.88782215}
{'transcript': '這是專題的測驗音檔剪接軟體的測試音檔'}
{'transcript': '這是專題的成音音檔剪接軟體的測試音檔'}
{'transcript': '這是專題的成因音檔剪接軟體的測試音檔'}
{'transcript': '這是專題的測驗音檔剪接單體的測試音檔'}
剪接
```