import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

sampling_freq, audio = wavfile.read(r"C:\Windows\media\Windows Background.wav")   # 讀取檔案

audio = audio / np.max(audio)   # 歸一化，標準化

# 應用傅立葉變換
fft_signal = np.fft.fft(audio)
print(fft_signal)
# [-0.04022912+0.j         -0.04068997-0.00052721j -0.03933007-0.00448355j
#  ... -0.03947908+0.00298096j -0.03933007+0.00448355j -0.04068997+0.00052721j]

fft_signal = abs(fft_signal)
print(fft_signal)
# [0.04022912 0.04069339 0.0395848  ... 0.08001755 0.09203427 0.12889393]

# 建立時間軸
Freq = np.arange(0, len(fft_signal))

# 繪製語音訊號的
plt.figure()
plt.plot(Freq, fft_signal, color='blue')
plt.xlabel('Freq (in kHz)')
plt.ylabel('Amplitude')
plt.show()