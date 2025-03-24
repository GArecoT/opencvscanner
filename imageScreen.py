from threading import Thread
from time import sleep, time
from tkinter import Tk, Label
from PIL import Image, ImageTk

photo = None
frame = None
photoTK = None
window = None

prevTime = time()

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
    global photo, frame, photoTK

    aspect_ratio = photo.width/photo.height

    if(window.width > window.height):
        newPhoto = photo.resize((int(window.height * aspect_ratio), window.height))
    else:
        newPhoto = photo.resize((window.width, int(window.width/ aspect_ratio)))
    photoTK = ImageTk.PhotoImage(image=newPhoto)
    frame.configure(image=photoTK)
    frame.image = photoTK

def spawnImageViewer(img):
    global photo, frame, photoTK
    root = Tk()
    root.title(img)
    frame = Label(root)
    photo = Image.open(img)
    photoTK = ImageTk.PhotoImage(image=photo)
    frame.configure(image=photoTK)
    frame.bind('<Configure>', lambda a: Thread(target=debounce, args=(a,)).start())
    frame.pack(fill='both', expand=True)
    root.mainloop()

# spawnImageViewer('')

