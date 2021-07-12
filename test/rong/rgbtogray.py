import numpy as np
import cv2 as cv

cap = cv.VideoCapture('media/hyiap-emio8.avi')

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('media/NEWoutput.avi', fourcc, 20.0, (960, 540), isColor=False)

while True :
    ret, frame = cap.read()
     # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    #frame = cv.flip(frame, 0)
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    # write the flipped frame
    out.write(frame)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()