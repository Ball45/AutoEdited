from moviepy.editor import VideoFileClip, concatenate_videoclips
clip1 = VideoFileClip("media/tainan1.MOV")
clip2 = VideoFileClip("media/tainan2.MOV")
clip3 = VideoFileClip("media/tainan3.MOV")
final_clip = concatenate_videoclips([clip1,clip2,clip3])
final_clip.write_videofile("media/tainanvlog.mp4")