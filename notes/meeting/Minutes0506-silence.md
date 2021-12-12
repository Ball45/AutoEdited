# 0506--Silence detection

## Install [Auditok](https://github.com/amsehili/auditok)
A basic version of auditok will run with standard Python (>=3.4). However, without installing additional dependencies, auditok can only deal with audio files in wav or raw formats. if you want more features, the following packages are needed:

- [pydub](https://github.com/jiaaro/pydub) : read audio files in popular audio formats (ogg, mp3, etc.) or extract audio from a video file.

## Basic example
```python
import auditok

# split returns a generator of AudioRegion objects
audio_regions = auditok.split(
    "media/tsat.mp3",
    min_dur=0.2,     # minimum duration of a valid audio event in seconds
    max_dur=4,       # maximum duration of an event
    max_silence=0.3, # maximum duration of tolerated continuous silence within an event
    energy_threshold=55 # threshold of detection
)

for i, r in enumerate(audio_regions):

    # Regions returned by `split` have 'start' and 'end' metadata fields
    
    print("Region  {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))

```
    
## Output non-silence detection
```
Region 0: 0.500s -- 3.150s
Region 1: 4.350s -- 6.650s
Region 2: 7.800s -- 9.950s
Region 3: 10.900s -- 13.250s
Region 4: 14.250s -- 16.400s
Region 5: 17.350s -- 19.400s
Region 6: 20.450s -- 22.550s
Region 7: 23.750s -- 25.800s
Region 8: 27.150s -- 29.000s
Region 9: 30.050s -- 32.500s

```

