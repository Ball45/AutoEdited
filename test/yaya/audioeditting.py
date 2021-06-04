from pydub import AudioSegment

file_name = r"media\\testb1.wav"
sound = AudioSegment.from_wav(file_name)

start_time = "0:0"
stop_time = "0:9"
print("time:", start_time, "~", stop_time)

start_time = (int(start_time.split(':')[0])
              * 60 + int(start_time.split(':')[1])) * 1000
stop_time = (int(stop_time.split(':')[0])
             * 60 + int(stop_time.split(':')[1])) * 1000

print("ms:", start_time, "~", stop_time)

word = sound[start_time:stop_time]
save_name = r"media\\" + "sound1" + file_name[-4:]
print(save_name)

word.export(save_name, format="mp3", tags={
            'artist': 'AppLeU0', 'album': save_name[:-4]})
