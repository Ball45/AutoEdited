from moviepy.editor import VideoFileClip
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

clip = VideoFileClip("media/tryf.mp4") 
clip1 = clip.subclip(0, 3) 
clip2 = clip.subclip(7, 9)
count=1
sum=0
new_frame = [] 

for frames in clip.iter_frames():
    #print (frames.shape)
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray)
    #print (gray.shape)
    new_frame.append(gray)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
    count+=1
print (count)
print (new_frame[4]- new_frame[0])
List_length = len(new_frame[4])
print(List_length,gray.shape[0],len(gray[0]))

#for i in range :
 #   sum=sum+new_frame[i]*new_frame[i]

#print(new_frame)
#print((new_frame[3]-new_frame[7])*(new_frame[3]-new_frame[7]))
#print([frames[0].max() for frames in clip.get_frame(3)])

