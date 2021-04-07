from moviepy.editor import *
import os
video1 = VideoFileClip("media/0001 (1).mp4").subclip(0, 8)
video2 = VideoFileClip("media/0001 (1).mp4").subclip(0, 8)
video3 = VideoFileClip("media/0001 (1).mp4").subclip(0, 8)
video4 = VideoFileClip("media/0001 (1).mp4").subclip(0, 8)

final_clip = clips_array([[video1, video2],
                          [video3, video4]])
final_clip.write_videofile("media/new.mp4")
