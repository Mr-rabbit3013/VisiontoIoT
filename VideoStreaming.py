import numpy as np
import cv2

isValid = True

captureLeft = cv2.VideoCapture(0)

if not captureLeft.isOpened()  :
    print("can't open the camera")


while(True):
    # Capture frame-by-frame
    try :
        retLeft, frameLeft = captureLeft.read()

    except:
        print("error the take a image")
        isValid = False


    if isValid == True:
        try:
            # Our operations on the frame come here
            grayLeft = cv2.cvtColor(frameLeft, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            cv2.imshow('frameLeft',cv2.line(grayLeft,(0,0),(511,511),(255,0,0),5))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            print("Error during the convertion")


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()