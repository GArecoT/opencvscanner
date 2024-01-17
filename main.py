import cv2
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

    #Toggle autofocus
    if keys == ord('f'):
        if vid.get(cv2.CAP_PROP_AUTOFOCUS) == 0.0:
            vid.set(cv2.CAP_PROP_AUTOFOCUS, 1.0)
            print("Autofocus on")
        elif vid.get(cv2.CAP_PROP_AUTOFOCUS) == 1.0:
            vid.set(cv2.CAP_PROP_AUTOFOCUS, 0.0)
            print("Autofocus off")

    #Control Focus
    if keys == ord('['):
        focus = vid.get(cv2.CAP_PROP_FOCUS)
        print("FOCUS: " + str(focus))
        vid.set(cv2.CAP_PROP_FOCUS, focus-5)
    if keys == ord(']'):
        focus = vid.get(cv2.CAP_PROP_FOCUS)
        print("FOCUS: " + str(focus))
        vid.set(cv2.CAP_PROP_FOCUS, focus+5)
    
    #Control exposure
    if keys == ord('u'):
        exposure = vid.get(cv2.CAP_PROP_EXPOSURE)
        print("EXPOSURE: " + str(exposure))
        vid.set(cv2.CAP_PROP_EXPOSURE, exposure-100)
    if keys == ord('i'):
        exposure = vid.get(cv2.CAP_PROP_EXPOSURE)
        print("EXPOSURE: " + str(exposure))
        vid.set(cv2.CAP_PROP_EXPOSURE, exposure+100)

    #Control brightness
    if keys == ord('o'):
        brightness = vid.get(cv2.CAP_PROP_BRIGHTNESS)
        print("BRIGHTNESS: " + str(brightness))
        vid.set(cv2.CAP_PROP_BRIGHTNESS, brightness-5)
    if keys == ord('p'):
        brightness = vid.get(cv2.CAP_PROP_BRIGHTNESS)
        print("BRIGHTNESS: " + str(brightness))
        vid.set(cv2.CAP_PROP_BRIGHTNESS, brightness+5)

    #Control gain 
    if keys == ord('j'):
        gain = vid.get(cv2.CAP_PROP_GAIN)
        print("GAIN: " + str(gain))
        vid.set(cv2.CAP_PROP_GAIN, gain-5)
    if keys == ord('k'):
        gain = vid.get(cv2.CAP_PROP_GAIN)
        print("GAIN: " + str(gain))
        vid.set(cv2.CAP_PROP_GAIN, gain+5)

    #Control contrast 
    if keys == ord('l'):
        contrast = vid.get(cv2.CAP_PROP_CONTRAST)
        print("CONTRAST: " + str(contrast))
        vid.set(cv2.CAP_PROP_CONTRAST, contrast-5)
    if keys == ord(';'):
        contrast = vid.get(cv2.CAP_PROP_CONTRAST)
        print("CONTRAST: " + str(contrast))
        vid.set(cv2.CAP_PROP_CONTRAST, contrast+5)
vid.release()
cv2.destroyAllWindows()
