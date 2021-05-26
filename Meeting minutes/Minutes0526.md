# 0526 -- update silence detecion & SpeechRecognition

## Detect silence duration
- [ ] how to detect command?
```python
import auditok
import numpy as np

record_start = np.zeros(100)
record_end = np.zeros(100)
duration = np.zeros(100)
num = 0

# split returns a generator of AudioRegion objects
audio_regions = auditok.split(
    "media/testb.wav",
    min_dur=0.2,        # minimum duration of a valid audio event in seconds
    max_dur=100,        # maximum duration of an event
    max_silence=2,      # maximum duration of tolerated continuous silence within an event
    energy_threshold=40 # threshold of detection
)

for i, r in enumerate(audio_regions):
    record_start[i] = r.meta.start
    record_end[i] = r.meta.end
     print("Speech  {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))
    num = num+1
for j in range(num-1): 
    duration[j] = record_start[j+1] - record_end[j]
    print("Silence :" ,round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ',duration[j])

       
    if duration[j-1]>2.5 and duration[j]>2.5 :  #若前後都有三秒的靜音
        print("instruction : " ,round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')
```
### OUTPUT
```output
Speech  0: 0.750s -- 7.250s
Speech  1: 9.800s -- 12.800s
Speech  2: 15.600s -- 18.458s
Silence : 7.25 s to 9.8 s, Duration :  2.5500000000000007
Silence : 12.8 s to 15.6 s, Duration :  2.8000000000000007
instruction :  9.8 s to 12.8 s
```

## Read file [show all](https://github.com/Uberi/speech_recognition/issues/383) 
- [ ] 如果show all ,要如何測要”剪接“？
```python
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

```
```output
Text:  {'alternative': [{'transcript': '這是專輯的聲音音檔剪接軟體的測試音檔', 'confidence': 0.88782221}, {'transcript': '這是專題的測驗音檔剪接軟體的測試音檔'}, {'transcript': '這是專題的成音音檔剪接軟體的測試音檔'}, {'transcript': '這是專題的成因音檔剪接軟體的測試音檔'}, {'transcript': '這是專題的測驗音檔剪接單體的測試音檔'}], 'final': True}
pass

```
