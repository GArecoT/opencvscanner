import cv2
import numpy as np

from controls import controls
cam_index = 2
focus = 400.0
contrast = 64.0
saturation = 30

#set initial paramethers
vid = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
vid.set(cv2.CAP_PROP_FPS, 10.0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1536)
vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
vid.set(cv2.CAP_PROP_AUTOFOCUS, 0.0)
vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0)

#set custom paramethers
vid.set(cv2.CAP_PROP_FOCUS, focus)
vid.set(cv2.CAP_PROP_CONTRAST, contrast)
vid.set(cv2.CAP_PROP_SATURATION, saturation)


while (True):
    ret, frame = vid.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(thresh,kernel,iterations=2)
    thresh = cv2.erode(imgDial,kernel,iterations=1)
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    def get_contour_areas(contours):

        all_areas= []

        for cnt in contours:
            area= cv2.contourArea(cnt)
            all_areas.append(area)

        return all_areas
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)


    largest_item= sorted_contours[0]

    image_copy = frame.copy()
    cv2.drawContours(image=image_copy, contours=largest_item, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    x,y,w,h = cv2.boundingRect(largest_item)
    ROI = frame[y:y+h, x:x+w]

    # see the results
    cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('custom window', image_copy)
    #cv2.imshow('None approximation', image_copy)
    keys = cv2.waitKey(1) & 0xFF
    if keys == ord('q'):
        break
    elif keys == ord("d"):
        cv2.imwrite('ROI.png',ROI)
    else:
        controls(vid,keys)
vid.release()
cv2.destroyAllWindows()
