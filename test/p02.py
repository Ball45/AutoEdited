from moviepy.editor import *

video1 = VideoFileClip("media/0001 (1).mp4").subclip(0,10)
video2 = VideoFileClip("media/0001 (1).mp4").subclip(0,10)
video3 = VideoFileClip("media//0001 (1).mp4").subclip(0,10)
video4 = VideoFileClip("media//0001 (1).mp4").subclip(0,10)

final_clip = clips_array([[video1, video2],
                          [video3, video4]])
final_clip.write_videofile("media/new.mp4")
