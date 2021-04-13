from moviepy.editor import VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("media/0001 (3).mp4").subclip(0, 5)
clip2 = VideoFileClip("media/0001 (3).mp4").subclip(0, 5)

finalclip = concatenate_videoclips([clip1, clip2])
finalclip.write_videofile("media/out.mp4")  # 寫出檔案out.mp4
