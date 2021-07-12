from moviepy.editor import VideoFileClip
from moviepy.editor import *
import numpy as np
import cv2

clip = VideoFileClip("media/tryf.mp4") 
source = cv2.VideoCapture('media/tryf.mp4')
  
# running the loop
while True:
  
    # extracting the frames
    ret, img = source.read()
      
    # converting to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    # displaying the video
    cv2.imshow("media/Live.mp4", gray)
  
    # exiting the loop
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
      
    
# closing the window
cv2.destroyAllWindows()
source.release()
      
f3 = [frames for frames in gray.get_frame(1)]
print('f3 : \n' ,f3[0],"\n",len(f3[0]))

for flames in gray.iter_frames():
    print(flames.shape)
    break;

f2 = [frames[0,:,0].max() for frames in clipblackwhite.iter_frames()]
#print('f2 : \n',f2)
#clipblackwhite.write_videofile("media/0708N.mp4")
#cv2.IMREAD_GRAYSCALE: 
#moviepy.video.fx.all.blackwhite

