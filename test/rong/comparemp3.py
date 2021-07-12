from moviepy.editor import VideoFileClip
#import numpy as np
import cv2 as cv

clip = VideoFileClip("media/tryf.mp4") 
clip1 = clip.subclip(0, 3) 
clip2 = clip.subclip(7, 9)
count=1
new_frame = [] 
for frames in clip.iter_frames():
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    new_frame.append(gray)
    #print (frames.shape)
    #print (gray.shape)
    count+=1
print (count)
print(new_frame[0])
print([frames[0] for frames in clip.get_frame(3.001)])

