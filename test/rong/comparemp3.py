import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

fft_signal1 = np.zeros(100000)
fft_signal2 = np.zeros(100000)

 # 讀取檔案
sampling_freq1, audio1 = wavfile.read(r"media/testc.wav")  
sampling_freq2, audio2 = wavfile.read(r"media/testb.wav")  



audio1 = audio1 / np.max(audio1)   # 歸一化，標準化
audio2 = audio2 / np.max(audio2)   # 歸一化，標準化

# 應用傅立葉變換
fft_signal1 = np.fft.fft(audio1)
print(fft_signal1)
fft_signal2 = np.fft.fft(audio2)
print(fft_signal2)
# [-0.04022912+0.j         -0.04068997-0.00052721j -0.03933007-0.00448355j
#  ... -0.03947908+0.00298096j -0.03933007+0.00448355j -0.04068997+0.00052721j]

fft_signal1 = abs(fft_signal1)
print(fft_signal1)
fft_signal2 = abs(fft_signal2)
print(fft_signal2)
# [0.04022912 0.04069339 0.0395848  ... 0.08001755 0.09203427 0.12889393]


# 建立時間軸
Freq1 = np.arange(0, len(fft_signal1))
Freq2 = np.arange(0, len(fft_signal2))
# 繪製語音訊號的
plt.figure()
plt.plot(Freq1, fft_signal1, color='blue')
plt.plot(Freq2, fft_signal2, color='red')
plt.xlabel('Freq (in kHz)')
plt.ylabel('Amplitude')
plt.show()