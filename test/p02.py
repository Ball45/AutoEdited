from moviepy.editor import *

video1 = VideoFileClip("media/501A.wmv").subclip(10,20)
video2 = VideoFileClip("media/501A.wmv").subclip(20,30)
video3 = VideoFileClip("media/501A.wmv").subclip(30,40)
video4 = VideoFileClip("media/501A.wmv").subclip(40,50)

final_clip = clips_array([[video1, video2],
                          [video3, video4]])
final_clip.write_videofile("media/new.mp4")
