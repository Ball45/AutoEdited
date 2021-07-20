
from moviepy.editor import VideoFileClip
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

clip = VideoFileClip("media\\airplane.mp4")
count = 0
fps = 30
sum = 0
summ = 0
new_frame = []


def square(a):
    for i in a:
        return i**2


for frames in clip.iter_frames():
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray)
    new_frame.append(gray)
    count += 1
    key = cv.waitKey(1)
    if key == ord("q"):
        break
print(count)

print('new_frame[0] : ', new_frame[0])
print('new_frame[270] : ', new_frame[270])

print(new_frame[0] - new_frame[4])
print(square(new_frame[270] - new_frame[0]))

# 平方和
# for i in square(new_frame[270]- new_frame[0]) :
#    sum=sum+i
# print(sum)

List_length = len(new_frame)
print(List_length, len(new_frame[0]), len(gray), len(
    gray[0]), len(square(new_frame[270] - new_frame[0])))
time = len(new_frame)/fps

# 比較第t秒和第7秒的frames，一秒鐘有30個frame(fps=30)
for t in range(int(time)):
    for k in range(fps):
        for j in square(new_frame[t+k] - new_frame[7+k]):
            summ = summ+j
    print('t : ', t, ' - 7 =', summ, '\n')
    summ = 0
