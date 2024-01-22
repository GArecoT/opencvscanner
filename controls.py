import cv2
from PIL import Image 
import os
from tkinter import simpledialog
from tkinter import messagebox
def controls(vid, key, cut, count):
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

        if key == 92:
            cv2.imwrite("./temp/" + str(str(count) + ".png"),cut)
            count = count + 1
            print("Page " + str(count) + " saved")
        if key == 103:
            images = []
            for i in range(count):
                temp = Image.open("./temp/"+str(i)+".png")
                images.append(temp)

            answer = simpledialog.askstring("Input", "File Name")
            
            #Check if file exists
            if(os.path.isfile("./pdf_output/"+str(answer).upper()+".pdf") == True):
                print("File already exists")
                messagebox.showinfo("ERROR","File already exists")                
            else:
                pdf_path = "./pdf_output/"+str(answer).upper()+".pdf"
                
                images[0].save(
                    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
                )
                
                count = 0
                print("File " + str(answer).upper() + ".pdf is saved!")    

                for filename in os.listdir('./temp/'):
                    if os.path.isfile(os.path.join('./temp/', filename)):
                     os.remove(os.path.join('./temp/', filename))
            
        if key == ord(','):
            return -90, count
        if key == ord('.'):
            return 90, count

        return 0, count

