from typing import ClassVar
import auditok
import numpy as np

record_start = np.zeros(10)
record_end = np.zeros(10)
num = 0

# split returns a generator of AudioRegion objects
audio_regions = auditok.split(
    "media\\OSRus.wav",
    min_dur=0.2,     # minimum duration of a valid audio event in seconds
    max_dur=4,       # maximum duration of an event
    max_silence=0.3,  # maximum duration of tolerated continuous silence within an event
    energy_threshold=55  # threshold of detection
)

# for i, r in enumerate(audio_regions):

# Regions returned by `split` have 'start' and 'end' metadata fields
# print("Region {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))

# play detection
# r.play(progress_bar=True)

# region's metadata can also be used with the `save` method
# (no need to explicitly specify region's object and `format` arguments)
# filename = r.save("media\\region_{meta.start:.3f}-{meta.end:.3f}.wav")
# print("region saved as: {}".format(filename))


for i, r in enumerate(audio_regions):
    record_start[i] = r.meta.start
    record_end[i] = r.meta.end
    num = num+1
for j in range(num-1):
    # print(str(record_start[j+1]) + 'to' + str(record_end[j]))
    # print(str(record_end[j]) + 'to' + str(record_start[j+1]))
    print(round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's')
