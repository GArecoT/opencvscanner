import cv2

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
    cv2.imshow('frame', frame)
    keys = cv2.waitKey(1) & 0xFF
    if keys == ord('q'):
        break
    else:
        controls(vid,keys)
vid.release()
cv2.destroyAllWindows()
