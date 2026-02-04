from threading import Thread
from time import sleep, time
from tkinter import Toplevel, Label
from PIL import Image, ImageTk
import os

photo = None
frame = None
photoTK = None
window = None
root = None
notification = None
localImg = 0

prevTime = time()

def viwerControls(key):
    global photo, frame, photoTK, root, localImg, notification
    # go to next pag
    if(key.keysym == 'Right'):
        root.title(str(localImg))
        localImg = int(localImg) + 1
        # check if image exists
        path = "./.temp/"+  str(localImg) +".png"
        if(os.path.isfile(path)):
            photo = Image.open(path)
            photoTK = ImageTk.PhotoImage(image=photo, master=root)
            frame.configure(image=photoTK)
            notification.config(text="Page" + str(localImg))
        else:
            localImg = int(localImg) - 1

    # go to prev pag
    if(key.keysym == 'Left'):
        root.title(str(localImg))
        localImg = int(localImg) - 1
        path = "./.temp/"+  str(localImg) +".png"
        if(os.path.isfile(path)):
            photo = Image.open(path)
            photoTK = ImageTk.PhotoImage(image=photo, master=root)
            frame.configure(image=photoTK)
            notification.config(text="Page" + str(localImg))
        else:
            localImg = int(localImg) + 1


def debounce(a):
    global prevTime, window
    prevTime = time() 
    window = a
    sleep(0.5)
    nextTime = time()
    timeA = nextTime - prevTime
    if(timeA >= 0.5):
        resize_image()


def resize_image():
    global photo, frame, photoTK, newPhoto, root

    aspect_ratio = photo.width/photo.height

    if(window.width > window.height):
        newPhoto = photo.resize((int(window.height * aspect_ratio), window.height))
    else:
        newPhoto = photo.resize((window.width, int(window.width/ aspect_ratio)))
    photoTK = ImageTk.PhotoImage(image=newPhoto)
    frame.configure(image=photoTK)
    frame.image = photoTK

def spawnImageViewer(img):
    global photo, frame, photoTK, root, localImg, notification
    localImg = int(img)
    root = Toplevel()
    root.title(str(localImg))
    root.attributes('-type', 'dialog')
    root.geometry("500x700")
    frame = Label(root)
    notification = Label(root, fg="#f5c2e7", bg="#313244")
    notification.place(x=10, y=10)
    photo = Image.open("./.temp/"+  str(localImg) +".png")
    # photo = Image.open(img)
    photoTK = ImageTk.PhotoImage(image=photo, master=root)
    frame.configure(image=photoTK)
    frame.bind('<Configure>', lambda a: Thread(target=debounce, args=(a,)).start())
    frame.pack(fill='both', expand=True)
    root.bind(
        "<Key>",
        lambda event: 
            viwerControls(event)
    )
    root.mainloop()


# spawnImageViewer('0')


