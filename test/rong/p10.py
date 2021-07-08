from moviepy.editor import VideoFileClip
import numpy as np


clip = VideoFileClip("media/0708.mp4") 
     
# getting only first 5 seconds 
clip1 = clip.subclip(0, 3) 
clip2 = clip.subclip(7, 10)
  
# iterating frames
frames1 = clip1.iter_frames()
frames2 = clip2.iter_frames() 

f1 = [frames1[0,:,0].max() for frames1 in clip1.iter_frames()]
f2 = [frames2[0,:,0].max() for frames2 in clip2.iter_frames()]


# counter to count the frames
counter1 = 0
counter2 = 0
  
# using loop to tranverse the frames
for value in frames1 :
    # incrementing the counter
    counter1 += 1

for value in frames2 :
    # incrementing the counter
    counter2 += 1

# printing the value of the counter
print("Counter Value ", end = " : ")
print(counter1,' ; ', counter2)
print ('frames1 : ',f1)
print ('frames2 : ',f2)
      
      

