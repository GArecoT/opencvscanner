import cv2
from PIL import Image, ImageTk
import os
from tkinter import simpledialog, messagebox, Tk, Label, Button
from threading import Thread
from createImage import spawnImageViewer

zerar = False
imgs = []

def saveFile(count, notification, bottomFrame, name = ''):
    global zerar, imgs
    images = []
    for i in range(count):
        temp = Image.open("./.temp/" + str(i) + ".png")
        images.append(temp)

    if len(images) > 0:
        dialogWindow = Tk()
        dialogWindow.withdraw()
        answer = simpledialog.askstring("Input", "File Name", parent=dialogWindow, initialvalue=name)
        dialogWindow.destroy()

        # If cancel return 
        if(answer == None):
            return

        # Check if file exists
        if os.path.isfile("./pdf_output/" + str(answer).upper() + ".pdf") == True:
            notification.config(text="File already exists")
            messagebox.showinfo("ERROR", "File already exists")
            saveFile(count, notification, bottomFrame, str(answer))
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

            for image in bottomFrame.winfo_children():
                image.destroy()
            zerar = True
            imgs = []
    else:
        messagebox.showinfo("ERROR", "No page scanned")


def controls(vid, key, cut, count, config, notification, bottomFrame, canvasImages, scroll, rootImgs):
    global zerar
    img = rootImgs

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
            bottomFrame.winfo_children()[len(bottomFrame.winfo_children()) - 1].destroy()
            imgs.pop()
            notification.config(text="Redo " + str(count + 1) + " page")

    # add page[count]
    if key.keysym == config.get("controls", "addpage"):  # this is the key code
        if(zerar == True):
            count = 0
            zerar = False
        # add page thumb
        img = cv2.cvtColor(cut, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        cv2.imwrite("./.temp/" + str(str(count) + ".png"), cut)

        h, w = img.size
        percentage = 100/h
        img = img.resize((int(h * percentage), int(w * percentage)))
        imgs.append(ImageTk.PhotoImage(img))
        button = Button(bottomFrame, image = imgs[count], 
                        command= lambda: spawnImageViewer(str(count - 1)))
        button.grid(row=0, column=count)
        count = count + 1
        
        # update canvas
        canvasImages.update_idletasks()
        canvasImages.configure( scrollregion=canvasImages.bbox("all"), 
                               xscrollcommand=scroll.set, height=100)
        canvasImages.itemconfigure('bottomFrame',height=100)

        notification.config(text="Page " + str(count) + " saved")
        canvasImages.xview_moveto(1)
    # save file
    if key.keysym == config.get("controls", "savefile"):  # this is the keycode
        Thread(target=saveFile, args=(count, notification, bottomFrame)).start()
        # imgs = []

        # bottomFrame.pack()
        # saveFile(count, notification)
        # x.start()
        # count = 0
    if key.keysym == (config.get("controls", "rotate-90")):
        return -90, count
    if key.keysym == (config.get("controls", "rotate+90")):
        return 90, count

    return 0, count
