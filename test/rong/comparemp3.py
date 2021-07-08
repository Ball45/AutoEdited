from moviepy.editor import VideoFileClip
import numpy as np

frame1 = np.array(100)
frame2 = np.array(100)
frame3 = np.array(100)
frame4 = np.array(100)
frame5 = np.array(100)
num = 1

myclip = VideoFileClip("media/0708.mp4") 

flame = myclip.subclip
frame5 = myclip.iter_frames()

for t in flame :
    frame = myclip.get_frame(num)
    print ('t =' , num , ' :\n' , frame)
    frame3 = frame1-frame
    frame4 = (frame3^2)+(frame5^2)
    print ('t^2= \n', frame4)
    num = num + 3
    


#print ( [frame[0,:,0].max()
 #            for frame in myclip.iter_frames()])

#print (myclip.get_frame(0.1))


#myclip.iter_frames()