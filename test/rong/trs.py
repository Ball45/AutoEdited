# importing the module
import cv2
from moviepy.editor import *
import numpy as np
  
# reading the vedio
source = cv2.VideoCapture('media/tryf.mp4')
new_frame = []  

# running the loop
#while True:
  
    # extracting the frames
ret, img = source.read()
      
    # converting to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #f1 = [frames.max() for frames in gray.get_frame(3)]
new_frame.append(gray)  
    #f2 = [frames for frames in clip.get_frame(7)]
    
    # displaying the video
cv2.imshow("Live", gray)
print(new_frame) 
    # exiting the loop
    #key = cv2.waitKey(1)
    #if key == ord("q"):
     #   break
    

# closing the window
#cv2.destroyAllWindows()
#source.release()
print ('Counter Value frames1 : ',len(new_frame))

