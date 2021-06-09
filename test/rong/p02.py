## from moviepy.editor import *
##import os
##video1 = VideoFileClip("media/0001 (1).mp4").subclip(0, 8)
##video2 = VideoFileClip("media/0001 (1).mp4").subclip(0, 8)
##video3 = VideoFileClip("media/0001 (1).mp4").subclip(0, 8)
##video4 = VideoFileClip("media/0001 (1).mp4").subclip(0, 8)

# final_clip = clips_array([[video1, video2],
# [video3, video4]])
# final_clip.write_videofile("media/new.mp4")

# 串連影片
from moviepy.editor 
import VideoFileClip, concatenate_videoclips
clip1 = VideoFileClip("media/airplane.mp4")
clip2 = VideoFileClip("media/thunder.mp4")
final_clip = concatenate_videoclips([clip1, clip2])
final_clip.write_videofile("media/test2.mp4")


from pydub import AudioSegment


def joinVoice():
    file1_name = r"../data/sound1.mp3"
    file2_name = r"../data/sound2.mp3"
    # 加载需要拼接的两个文件
    sound1 = AudioSegment.from_mp3(file1_name)
    sound2 = AudioSegment.from_mp3(file2_name)
    # 取得两个文件的声音分贝
    db1 = sound1.dBFS
    db2 = sound2.dBFS
    dbplus = db1 - db2
    # 声音大小
    if dbplus < 0:
        sound1 += abs(dbplus)
    else:
        sound2 += abs(dbplus)
    # 拼接两个音频文件
    finSound = sound1 + sound2
    save_name = r"../data/" + "finSound" + file1_name[-4:]
    print("save_path:", save_name)

    finSound.export(save_name, format="mp3", tags={'artist': 'AppLeU0', 'album': save_name[:-4]})
    return True
if __name__ == '__main__':
    joinVoice()

————————————————
版权声明：本文为CSDN博主「Solarzhou」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ZT7524/article/details/104280794