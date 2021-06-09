# cutaudio
- [reference1](https://twgreatdaily.com/JT0EhXEBfwtFQPkd643n.html)
- [reference2](https://blog.csdn.net/ZT7524/article/details/104280794)
- 可以將空白檢調，變成更完整的影片。

```python
from pydub import AudioSegment

# 1秒=1000毫秒
SECOND = 1000
# 導入音樂
file1_name = r"media/testc.wav"
file2_name = r"media/testc.wav"
sound = AudioSegment.from_wav(file1_name)
#sound2 = AudioSegment.from_wav(file2_name)

# 取33秒到70秒間的片段
sound1 = sound[14.3*SECOND:20.9*SECOND]
sound2 = sound[24.75*SECOND:27.75*SECOND]

# 拼接两个音频文件
finSound = sound1 + sound2
print("save_path:")

# 導出音樂
finSound.export("media/finsound.mp3")
```

# update silence
- 增加一個條件使他不會偵測到中間的speech，可以更準確的抓到指令。

```python
import auditok
import numpy as np

record_start = np.zeros(100)
record_end = np.zeros(100)
duration = np.zeros(100)
speech = np.zeros(100)
num = 0

# split returns a generator of AudioRegion objects
audio_regions = auditok.split(
    "media/testc.wav",
    min_dur=0.2,        # minimum duration of a valid audio event in seconds
    max_dur=100,        # maximum duration of an event
    max_silence=2,      # maximum duration of tolerated continuous silence within an event
    energy_threshold=40 # threshold of detection
)

for i, r in enumerate(audio_regions):
    record_start[i] = r.meta.start
    record_end[i] = r.meta.end
    speech[i] = record_end[i] - record_start[i]
    print("Speech  {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r) , "Duration : ", speech[i])
    num = num+1

for j in range(num-1):
    duration[j] = record_start[j+1] - record_end[j]
    
    print("Silence ", j, " :" ,round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ',duration[j])

    if duration[j-1] > 2.5 and duration[j] > 2.5 and speech[j] < 5.0:
        print("instruction : " ,round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')
```
OUTPUT
```
Speech  0: 1.250s -- 5.950s Duration :  4.7
Speech  1: 8.750s -- 11.500s Duration :  2.75
Speech  2: 14.300s -- 20.900s Duration :  6.599999999999998
Speech  3: 24.750s -- 27.450s Duration :  2.6999999999999993
Speech  4: 30.800s -- 33.993s Duration :  3.1925623582766427
Silence  0  : 5.95 s to 8.75 s, Duration :  2.8
Silence  1  : 11.5 s to 14.3 s, Duration :  2.8000000000000007
instruction :  8.75 s to 11.5 s
Silence  2  : 20.9 s to 24.75 s, Duration :  3.8500000000000014
Silence  3  : 27.45 s to 30.8 s, Duration :  3.3500000000000014
instruction :  24.75 s to 27.45 s
```