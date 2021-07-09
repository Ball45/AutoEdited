# importing matplotlib
from matplotlib import pyplot as plt
  
# importing numpy
import numpy as np
  
# Import everything needed to edit video clips
from moviepy.editor import *
  
# loading video gfg
clip = VideoFileClip("media/0708.mp4")

# getting only first 5 seconds
#clip = clip.subclip(5, 10)
  
# getting frame at time 3
frame = clip.get_frame(10)
frame2 = clip.get_frame(1)
f1 = [frames.max() for frames in clip.get_frame(3)]
f2 = [frames for frames in clip.get_frame(7)]
print ('Counter Value frames1 : ',len(f1))
print ('Counter Value frames2 : ',len(f2))
print(f1)  
#print(f2)

for t in range(0):
    #f1=[t for i in range(len(f2))]
   
   # back(f2) minus front(f1)
    new_frame = []  
    sum = 0
    for i in range(len(f2)):
        new_value = f2[i] - f1[i]
        sum=sum+new_value^2
        new_frame.append(new_value)    
        
    #print (new_frame)
    #print (sum)
    t+=1

# showing the frame with the help of matplotlib
#plt.imshow(frame, interpolation ='nearest')
  
# show
#plt.show()