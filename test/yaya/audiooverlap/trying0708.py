import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

audio_path = 'media\\2021-08-27.wav'
y, sr = librosa.load(audio_path, sr=22200)
librosa.feature.melspectrogram(y=y, sr=sr)

D = np.abs(librosa.stft(y))**2
S = librosa.feature.melspectrogram(S=D, sr=sr)

S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                    fmax=8000)

#用matplotlib輸出圖片
fig, ax = plt.subplots()
S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time',
                         y_axis='mel', sr=sr,
                         fmax=8000, ax=ax)
fig.colorbar(img, ax=ax, format='%+2.0f dB')
ax.set(title='Mel-frequency spectrogram')
plt.show()















# # prints the maximum of red that is contained
# # on the first line of each frame of the clip.
# from moviepy.editor import VideoFileClip
# myclip1 = VideoFileClip('media\\07082.mp4').subclip(0, 2)
# myclip2 = VideoFileClip('media\\07082.mp4').subclip(5, 7)
# print("1:", [frame[0, :, 0].max()for frame in myclip1.iter_frames()], '\n'
#       "2:", [frame[0, :, 0].max()for frame in myclip2.iter_frames()]
#       )
