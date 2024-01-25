import cv2
from controls import controls
from imageprocess import image_process
from createConfig import createConfig, checkConfig
import configparser

#Config file
config = configparser.ConfigParser()
createConfig(config)
checkConfig(config)
config.read('./config.ini')

#load default values
cam_index = int(config.get('camera_default', 'cam_index')) 
focus = float(config.get('camera_default', 'focus'))
contrast = float(config.get('camera_default', 'contrast'))
saturation = float(config.get('camera_default', 'saturation'))
rotation = float(config.get('camera_default', 'rotation'))
fps = float(config.get('camera_default', 'fps'))
width = int(config.get('camera_default', 'width'))
height = int(config.get('camera_default', 'height'))

global count
count = 0

#set linux or windows camera API
if(config.get('camera_default', 'os') == 'windows'):
    vid = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
elif(config.get('camera_default', 'os') == 'linux'):
    vid = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
else:
    print("Invalid OS value. Try windows or linux.")
    exit() 

#set initial paramethers
vid.set(cv2.CAP_PROP_FPS, fps)
vid.set(cv2.CAP_PROP_POS_FRAMES, fps)
vid.set(cv2.CAP_PROP_FRAME_COUNT, fps)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
vid.set(cv2.CAP_PROP_AUTOFOCUS, 0.0)
vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0)

#set custom paramethers
vid.set(cv2.CAP_PROP_FOCUS, focus)
vid.set(cv2.CAP_PROP_CONTRAST, contrast)
vid.set(cv2.CAP_PROP_SATURATION, saturation)


while (True):
    ret, frame = vid.read()
    image_copy, cut = image_process(frame, rotation)


    keys = cv2.waitKey(1) & 0xFF
    if keys == ord('q'):
        break
    else:
        temp, count = controls(vid, keys, cut, count, config)
        rotation += temp
        if rotation == 360:
            rotation = 0
        elif rotation == -90:
            rotation = 270

    # render window
    cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('custom window', image_copy)
    #cv2.imshow('None approximation', image_copy)
vid.release()
cv2.destroyAllWindows()
