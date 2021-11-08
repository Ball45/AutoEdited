import librosa

y, sr = librosa.load('media\\2021-08-27.wav')
librosa.feature.mfcc(y=y, sr=sr)