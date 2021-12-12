# spectrogram
import librosa

import matplotlib.pyplot as plt
import librosa.display

# import cv2
# from scipy.ndimage.morphology import binary_closing


audio_path = 'media\\2021-08-27.wav'

y , sr = librosa.load(audio_path, sr=22200)
# mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

Y = librosa.stft(y)
Xdb = librosa.amplitude_to_db(abs(Y))
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()

# ret, img = source.read()
# gray = cv2.cvtColor(plt.colorbar(), cv2.COLOR_BGR2GRAY) 


# plt.figure(figsize=(14, 5))
librosa.display.waveplot(y, sr=sr)
plt.show() #才有圖片


# import matplotlib.pyplot as plt
# import numpy as np

# x = np.linspace(0, 20, 100)
# plt.plot(x, np.sin(x))
# plt.show()


# amplitude envelope
# import librosa

# import matplotlib.pyplot as plt
# import librosa.display

# audio_path = 'media\\2021-08-27.wav'
# x , sr = librosa.load(audio_path, )
# print(type(x), type(sr))
# # <class 'numpy.ndarray'> <class 'int'>
# print(x.shape, sr)
# # (396688,) 22050

# plt.figure(figsize=(14, 5))
# librosa.display.waveplot(x, sr=sr)
# plt.show() #才有圖片


#　example 1
# # Beat tracking example
# import librosa

# # 1. Get the file path to an included audio example
# # filename = librosa.load("media\\2021-08-27.wav")

# # 2. Load the audio as a waveform `y`
# #    Store the sampling rate as `sr`
# y, sr = librosa.load("media\\2021-08-27.wav")

# # 3. Run the default beat tracker
# tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

# # 4. Convert the frame indices of beat events into timestamps
# beat_times = librosa.frames_to_time(beat_frames, sr=sr)






# import os
# songmp4 = "media\\NewRecording7.m4a"
# songwav = "media\\NewRecording7.wav"
# os.system("ffmpeg -i "+songmp4+" "+songwav)


## import os

##　mp4file = "media\\shallow.mp4"
##  mp3file = "media\\guitar.mp3"
##  os.system("ffmpeg -i "+mp4file+" "+mp3file)
