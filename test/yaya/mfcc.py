import soundfile as sf

data, samplerate = sf.read('media\\2021-08-27.wav')
sf.write('new_file.flac', data, samplerate)