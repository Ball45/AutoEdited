
# prints the maximum of red that is contained
# on the first line of each frame of the clip.
from moviepy.editor import VideoFileClip
myclip1 = VideoFileClip('media\\07082.mp4').subclip(0, 2)
myclip2 = VideoFileClip('media\\07082.mp4').subclip(5, 7)
print("1:", [frame[0, :, 0].max()for frame in myclip1.iter_frames()], '\n'
      "2:", [frame[0, :, 0].max()for frame in myclip2.iter_frames()]
      )
