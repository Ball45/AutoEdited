from moviepy.editor import VideoFileClip
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

clip = VideoFileClip("media/tryf.mp4") 
clip1 = clip.subclip(0, 3) 
clip2 = clip.subclip(7, 9)
count=0
sum=0
summ=0
new_frame = [] 

def square(a):
    for i in a: 
        return i**2

for frames in clip.iter_frames():
    #print (frames.shape)
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray)
    #print (gray.shape)
    new_frame.append(gray)
    count+=1
    key = cv.waitKey(1)
    if key == ord("q"):
        break
    
print (count)
print('new_frame[0] : ',new_frame[0])
print('new_frame[4] : ',new_frame[4])
#print('new_frame[0]^2 : ',square(new_frame[0]))
#print('new_frame[4] : ',square(new_frame[4]))
print (new_frame[0]- new_frame[4])
print (square(new_frame[4]- new_frame[0]))
for i in square(new_frame[4]- new_frame[0]) :
    sum=sum+i
print(sum)
List_length = len(new_frame)
print(List_length,len(gray),len(gray[0]))

for i in range(10):
    for j in square(new_frame[i]- new_frame[7]) :
        summ=summ+j
    print('t : ',i,' - 7 =', summ, '\n')
    summ=0



#for i in range :
 #   sum=sum+new_frame[i]*new_frame[i]

#print(new_frame)
#print((new_frame[3]-new_frame[7])*(new_frame[3]-new_frame[7]))
#print([frames[0].max() for frames in clip.get_frame(3)])

