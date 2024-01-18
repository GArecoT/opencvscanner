import cv2
import numpy as np
def image_process(frame):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(thresh,kernel,iterations=2)
    thresh = cv2.erode(imgDial,kernel,iterations=1)
    contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    image_copy = frame.copy()
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    if(len(sorted_contours)>0):
        largest_item= sorted_contours[0]
        cv2.drawContours(image=image_copy, contours=largest_item, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        x,y,w,h = cv2.boundingRect(largest_item)
        cut = frame[y:y+h, x:x+w]
    else:
        cut = image_copy
    
    return image_copy, cut

