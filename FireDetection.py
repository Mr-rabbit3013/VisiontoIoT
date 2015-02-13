import numpy as np
import cv2
import PIL.Image

cap = cv2.VideoCapture('samples/fBackYardFire.avi')

fgbg = cv2.BackgroundSubtractorMOG()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    img = PIL.Image.fromarray(frame)



    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    fgmask = fgbg.apply(frame)

    print frame

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()