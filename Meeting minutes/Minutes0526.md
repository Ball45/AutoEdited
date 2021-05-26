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

        #若前後都有三秒的靜音
    if duration[j-1]>2.5 and duration[j]>2.5 :
        print("instruction : " ,round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')
```

## Read file show all
- [ ] 如果show all 偵測不到剪接?
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

