from pydub import AudioSegment

# 1秒=1000毫秒
SECOND = 1000
# 導入音樂
file1_name = r"media/testc.wav"
file2_name = r"media/testc.wav"
sound = AudioSegment.from_wav(file1_name)
#sound2 = AudioSegment.from_wav(file2_name)
a=14.3
b=20.9
# 取33秒到70秒間的片段
sound1 = sound[a*SECOND:b*SECOND]
sound2 = sound[24.75*SECOND:27.75*SECOND]

# 拼接两个音频文件
#finSound = sound1 + sound2
print("save_path:")

# 導出音樂
sound1.export("media/finsound.wav")




