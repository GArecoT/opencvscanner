import cv2
import numpy as np

from controls import controls
from imageprocess import image_process
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
    image_copy, cut = image_process(frame)

    # render window
    cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('custom window', image_copy)
    #cv2.imshow('None approximation', image_copy)
    keys = cv2.waitKey(1) & 0xFF
    if keys == ord('q'):
        break
    else:
        controls(vid,keys, cut)
vid.release()
cv2.destroyAllWindows()
