from moviepy.editor import VideoFileClip
import numpy as np
import cv2

clip = VideoFileClip("media/tryf.mp4") 
source = cv2.VideoCapture('media/tryf.mp4')

ret, img = source.read()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# getting only first 5 seconds 
clip1 = clip.subclip(0, 3) 
clip2 = clip.subclip(7, 9)
  
# iterating frames
frames1 = clip1.iter_frames()
frames2 = clip2.iter_frames() 

f1 = [frames1[0,:,0].max() for frames1 in clip1.iter_frames()]
f2 = [frames2[0,:,0].max() for frames2 in clip2.iter_frames()]

# getting frame at time 3
frame11 = clip1.get_frame(3)

# printing the value of the counter
print ('Counter Value frames1 : ',len(f1))
print ('Counter Value frames2 : ',len(f2))



#for t in range(2):
 #   f1=[t for i in range(len(f2))]
   
   # back(f2) minus front(f1)
  #  new_frame = []  
   # for i in range(len(f2)):
    #    new_value = f2[i] - f1[i]
     #   new_frame.append(new_value)    
    #print (new_frame)
    #t+=1




      
      

