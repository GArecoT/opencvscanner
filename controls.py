import cv2
from PIL import Image
import os
from tkinter import simpledialog, messagebox, Tk
from threading import Thread


def saveFile(count, notification):
    images = []
    for i in range(count):
        temp = Image.open("./.temp/" + str(i) + ".png")
        images.append(temp)

    if len(images) > 0:
        dialogWindow = Tk()
        dialogWindow.withdraw()
        answer = simpledialog.askstring("Input", "File Name", parent=dialogWindow)
        dialogWindow.destroy()

        # Check if file exists
        if os.path.isfile("./pdf_output/" + str(answer).upper() + ".pdf") == True:
            notification.config(text="File already exists")
            messagebox.showinfo("ERROR", "File already exists")
            saveFile(count, notification)
        else:
            pdf_path = "./pdf_output/" + str(answer).upper() + ".pdf"

            images[0].save(
                pdf_path,
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=images[1:],
            )

            notification.config(text="File " + str(answer).upper() + ".pdf is saved!")

            for filename in os.listdir("./.temp/"):
                if os.path.isfile(os.path.join("./.temp/", filename)):
                    os.remove(os.path.join("./.temp/", filename))
    else:
        messagebox.showinfo("ERROR", "No page scanned")


def controls(vid, key, cut, count, config, notification):

    if key.keysym == (config.get("controls", "toggleautoexposure")):
        if vid.get(cv2.CAP_PROP_AUTO_EXPOSURE) == 3.0:
            vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1.0)
            notification.config(text="Auto Exposure Off")
        elif vid.get(cv2.CAP_PROP_AUTO_EXPOSURE) == 1.0:
            vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3.0)
            notification.config(text="Auto Exposure On")

    # Toggle autofocus
    if key.keysym == (config.get("controls", "toggleautofocus")):
        if vid.get(cv2.CAP_PROP_AUTOFOCUS) == 0.0:
            vid.set(cv2.CAP_PROP_AUTOFOCUS, 1.0)
            notification.config(text="Autofocus on")
        elif vid.get(cv2.CAP_PROP_AUTOFOCUS) == 1.0:
            vid.set(cv2.CAP_PROP_AUTOFOCUS, 0.0)
            notification.config(text="Autofocus off")

    # Control Focus
    if key.keysym == (config.get("controls", "focus-")):
        focus = vid.get(cv2.CAP_PROP_FOCUS)
        vid.set(cv2.CAP_PROP_FOCUS, focus - 5)
        focus = vid.get(cv2.CAP_PROP_FOCUS)
        notification.config(text="FOCUS: " + str(focus))
    if key.keysym == (config.get("controls", "focus+")):
        focus = vid.get(cv2.CAP_PROP_FOCUS)
        vid.set(cv2.CAP_PROP_FOCUS, focus + 5)
        focus = vid.get(cv2.CAP_PROP_FOCUS)
        notification.config(text="FOCUS: " + str(focus))

    # Control exposure
    if key.keysym == (config.get("controls", "exposure-")):
        exposure = vid.get(cv2.CAP_PROP_EXPOSURE)
        vid.set(cv2.CAP_PROP_EXPOSURE, exposure - 100)
        exposure = vid.get(cv2.CAP_PROP_EXPOSURE)
        notification.config(text="EXPOSURE: " + str(exposure))
    if key.keysym == (config.get("controls", "exposure+")):
        exposure = vid.get(cv2.CAP_PROP_EXPOSURE)
        vid.set(cv2.CAP_PROP_EXPOSURE, exposure + 100)
        exposure = vid.get(cv2.CAP_PROP_EXPOSURE)
        notification.config(text="EXPOSURE: " + str(exposure))

    # Control brightness
    if key.keysym == (config.get("controls", "brightness-")):
        brightness = vid.get(cv2.CAP_PROP_BRIGHTNESS)
        vid.set(cv2.CAP_PROP_BRIGHTNESS, brightness - 5)
        brightness = vid.get(cv2.CAP_PROP_BRIGHTNESS)
        notification.config(text="BRIGHTNESS: " + str(brightness))
    if key.keysym == (config.get("controls", "brightness+")):
        brightness = vid.get(cv2.CAP_PROP_BRIGHTNESS)
        vid.set(cv2.CAP_PROP_BRIGHTNESS, brightness + 5)
        brightness = vid.get(cv2.CAP_PROP_BRIGHTNESS)
        notification.config(text="BRIGHTNESS: " + str(brightness))

    # Control gain
    if key.keysym == (config.get("controls", "gain-")):
        gain = vid.get(cv2.CAP_PROP_GAIN)
        vid.set(cv2.CAP_PROP_GAIN, gain - 5)
        gain = vid.get(cv2.CAP_PROP_GAIN)
        notification.config(text="GAIN: " + str(gain))
    if key.keysym == (config.get("controls", "gain+")):
        gain = vid.get(cv2.CAP_PROP_GAIN)
        vid.set(cv2.CAP_PROP_GAIN, gain + 5)
        gain = vid.get(cv2.CAP_PROP_GAIN)
        notification.config(text="GAIN: " + str(gain))

    # Control contrast
    if key.keysym == (config.get("controls", "contrast-")):
        contrast = vid.get(cv2.CAP_PROP_CONTRAST)
        vid.set(cv2.CAP_PROP_CONTRAST, contrast - 5)
        contrast = vid.get(cv2.CAP_PROP_CONTRAST)
        notification.config(text="CONTRAST: " + str(contrast))
    if key.keysym == (config.get("controls", "contrast+")):
        contrast = vid.get(cv2.CAP_PROP_CONTRAST)
        vid.set(cv2.CAP_PROP_CONTRAST, contrast + 5)
        contrast = vid.get(cv2.CAP_PROP_CONTRAST)
        notification.config(text="CONTRAST: " + str(contrast))

    # redo page
    if key.keysym == config.get("controls", "redopage"):  # this is the key code
        if count > 0:
            count = count - 1
            notification.config(text="Redo " + str(count + 1) + " page")

    # add page
    if key.keysym == config.get("controls", "addpage"):  # this is the key code
        cv2.imwrite("./.temp/" + str(str(count) + ".png"), cut)
        count = count + 1
        notification.config(text="Page " + str(count) + " saved")
    # save file
    if key.keysym == config.get("controls", "savefile"):  # this is the keycode
        Thread(target=saveFile, args=(count, notification)).start()
        # saveFile(count, notification)
        # x.start()
        count = 0
    if key.keysym == (config.get("controls", "rotate-90")):
        return -90, count
    if key.keysym == (config.get("controls", "rotate+90")):
        return 90, count

    return 0, count
