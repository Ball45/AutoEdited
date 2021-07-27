
from moviepy.editor import VideoFileClip
import numpy as np
import cv2 as cv


clip = VideoFileClip("media/testtt.mp4")
cut1= clip.subclip(0,3)
cut2= clip.subclip(7,12)
count = 0
fps = 30
sum = 0
summ = 0
new_frame1 = []
new_frame2 = []


#轉灰階
for frames in cut1.iter_frames():
    #print(frames.shape)
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray) #播放灰階影片
    #print(gray.shape)
    new_frame1.append(gray)
    count += 1
    key = cv.waitKey(1)
    if key == ord("q"):
        break
print('number of frames: ', count)
time = count/fps

for frames in cut2.iter_frames():
    #print(frames.shape)
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray) #播放灰階影片
    #print(gray.shape)
    new_frame2.append(gray)
    count += 1
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# frame size
print('frame size : W =', len(gray[0]), 'H =', len(new_frame[0]))

#測試加減、平方有沒有錯
#print('new_frame[0] : ', new_frame[0])
#print('new_frame[270] : ', new_frame[270])

#測試減法
#xx=new_frame[270] - new_frame[0]
#print(xx)

#測試平方
#yy=np.square(new_frame[0] - new_frame[270])
#print(yy)
#print(len(yy),len(yy[0]),len(xx),len(xx[2]))


min = 1000000
# 比較第t秒和第cutpoint秒的frames，一秒鐘有30個frame(fps=30)
for cutpoint in new_frame2 :
    for front in new_frame1 :
        for k in range(fps+30):
            for i in np.square(new_frame1[i+k] - new_frame2[i+k]):
                sum = sum + i
        print('t : ', t, ' - ',cutpoint,' =', summ, '\n')
        if min>summ:
            t1=t
            t2=cutpoint
            min=summ   
        sum = 0
        summ = 0
#輸出t1和t2最相近
print (t1,t2,min)


