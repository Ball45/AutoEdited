from moviepy.editor import VideoFileClip
from moviepy.editor import *
import numpy as np
import cv2

clip = VideoFileClip("media/0708.mp4").subclip(0,1)
f1 = [frames[0,:,0].max() for frames in clip.iter_frames()]

print('f1 : \n',f1,'\n',len(f1))

clipblackwhite = clip.fx(vfx.blackwhite)
clipgray = VideoFileClip("media/0708N.mp4")
f3 = [frames for frames in clipblackwhite.get_frame(1)]
print('f3 : \n' ,f3[0],"\n",len(f3[0]))

for flames in clipgray.iter_frames():
    print(flames.shape)
    break;

f2 = [frames[0,:,0].max() for frames in clipblackwhite.iter_frames()]
#print('f2 : \n',f2)
#clipblackwhite.write_videofile("media/0708N.mp4")
cv2.IMREAD_GRAYSCALE: 