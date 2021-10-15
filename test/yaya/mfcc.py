
from numpy import sign
from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
mfcc(sign, samplerate=16000, winlen=0.2, winstep=0.01, numcep=13, nfilt=26, 
nfft=512, lowfreq=0, highfreq=None, preemph=0.97, ceplifter=22, appendEnergy=True, 
winfunc=10)
(rate,sig) = wav.read("media\\NewRecording7.wav")
mfcc_feat = mfcc(sig,rate)
fbank_feat = logfbank(sig,rate)

print(fbank_feat[1:3,:])