# importing the module
import cv2
  
# reading the vedio
source = cv2.VideoCapture('media/res.png')
  
# running the loop
while True:
  
    # extracting the frames
    ret, img = source.read()
      
    # converting to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    #save it
    cv2.imwrite("media/NEWRe.png",gray)

    # displaying the video
    cv2.imshow("Live", gray)
  
    cv2.waitKey(0)
    cv2.destroyAllWindows()
      
# closing the window
cv2.destroyAllWindows()
source.release()

