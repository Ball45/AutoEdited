# import librosa
import librosa.display 
import matplotlib.pyplot as plt
x , sr = librosa.load("media\\2021-08-27.wav", sr=8000)
X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X))   # 把幅度轉成分貝格式
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()