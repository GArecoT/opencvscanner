import cv2
def controls(vid, key, cut):
        #Toggle autofocus
        if key == ord('f'):
            if vid.get(cv2.CAP_PROP_AUTOFOCUS) == 0.0:
                vid.set(cv2.CAP_PROP_AUTOFOCUS, 1.0)
                print("Autofocus on")
            elif vid.get(cv2.CAP_PROP_AUTOFOCUS) == 1.0:
                vid.set(cv2.CAP_PROP_AUTOFOCUS, 0.0)
                print("Autofocus off")

        #Control Focus
        if key == ord('['):
            focus = vid.get(cv2.CAP_PROP_FOCUS)
            print("FOCUS: " + str(focus))
            vid.set(cv2.CAP_PROP_FOCUS, focus-5)
        if key == ord(']'):
            focus = vid.get(cv2.CAP_PROP_FOCUS)
            print("FOCUS: " + str(focus))
            vid.set(cv2.CAP_PROP_FOCUS, focus+5)
        
        #Control exposure
        if key == ord('u'):
            exposure = vid.get(cv2.CAP_PROP_EXPOSURE)
            print("EXPOSURE: " + str(exposure))
            vid.set(cv2.CAP_PROP_EXPOSURE, exposure-100)
        if key == ord('i'):
            exposure = vid.get(cv2.CAP_PROP_EXPOSURE)
            print("EXPOSURE: " + str(exposure))
            vid.set(cv2.CAP_PROP_EXPOSURE, exposure+100)

        #Control brightness
        if key == ord('o'):
            brightness = vid.get(cv2.CAP_PROP_BRIGHTNESS)
            print("BRIGHTNESS: " + str(brightness))
            vid.set(cv2.CAP_PROP_BRIGHTNESS, brightness-5)
        if key == ord('p'):
            brightness = vid.get(cv2.CAP_PROP_BRIGHTNESS)
            print("BRIGHTNESS: " + str(brightness))
            vid.set(cv2.CAP_PROP_BRIGHTNESS, brightness+5)

        #Control gain 
        if key == ord('j'):
            gain = vid.get(cv2.CAP_PROP_GAIN)
            print("GAIN: " + str(gain))
            vid.set(cv2.CAP_PROP_GAIN, gain-5)
        if key == ord('k'):
            gain = vid.get(cv2.CAP_PROP_GAIN)
            print("GAIN: " + str(gain))
            vid.set(cv2.CAP_PROP_GAIN, gain+5)

        #Control contrast 
        if key == ord('l'):
            contrast = vid.get(cv2.CAP_PROP_CONTRAST)
            print("CONTRAST: " + str(contrast))
            vid.set(cv2.CAP_PROP_CONTRAST, contrast-5)
        if key == ord(';'):
            contrast = vid.get(cv2.CAP_PROP_CONTRAST)
            print("CONTRAST: " + str(contrast))
            vid.set(cv2.CAP_PROP_CONTRAST, contrast+5)

        if key == ord('s'):
            cv2.imwrite('teste.png',cut)

