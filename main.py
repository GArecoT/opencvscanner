from threading import Thread
from tkinter import messagebox, Tk, Canvas, Button, Frame, Label, OptionMenu, StringVar
from PIL import Image, ImageTk 
import cv2 
from controls import controls
from imageprocess import image_process
from createConfig import createConfig, checkConfig, creatFolders
import configparser
from listCamera import createCameraList

# Functions
#set aspect ratio
def resize_image():
    width = canvas.winfo_width()
    height = int(canvas.winfo_width() / aspect_ratio)
    if(height < 1):
        height = 1

    if(width > canvas.winfo_height()):
        width = canvas.winfo_height()
        height = int(canvas.winfo_height() / aspect_ratio)

   
    return width, height


def handle_zoom(event):
    print(event)
    global zoom_factor
    if(event.num == 4):
        zoom_factor += 1
    if(event.num == 5):
        if(zoom_factor > 1):
            zoom_factor -= 1


#handle rotation and add page
def handleRotation(response):
    global count
    global rotation 
    temp = response[0]
    count = response[1]
    rotation += temp
    if rotation == 360:
        rotation = 0
    elif rotation == -90:
        rotation = 270

def photo_image(img):
    global rotation
    w, h = resize_image()
    if(int(rotation) == 90 or int(rotation) == 270):
        imagePIL = Image.fromarray(img).resize((h,w))
    else:
        imagePIL = Image.fromarray(img).resize((w,h))
    imgtk = ImageTk.PhotoImage(image = imagePIL)

    #WARNING: This is shit, change it in the future
    imgtk = imgtk._PhotoImage__photo.zoom(zoom_factor)
    return imgtk

def update():
    global cut
    global notification
    ret, frame = vid.read()
    image_copy, cut = image_process(frame, rotation)

    if ret:
        photo = photo_image(image_copy)
        canvas.create_image(canvas.winfo_width()/2, 0, image=photo, anchor='n')
        canvas.image = photo
    root.after(15, update)
#set camera
def set_camera(cam_index):
    print(cam_index)
    global vid
    #set linux or windows camera API
    if(config.get('camera_default', 'os') == 'windows'):
        vid = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    elif(config.get('camera_default', 'os') == 'linux'):
        vid = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
    else:
        print("Invalid OS value. Try windows or linux.")
        exit() 
#camera change
def change_camera(*args):
    temp = selectedCamera.get().split(':')
    set_camera(int(temp[0]))
    try:
        update()
    except:
        messagebox.showerror('Error',"Camera not acessible. Please change the index.")


# Start setup
#list cameras
cameraList = createCameraList()
cameraListFormated = []

for camera in cameraList:
    cameraListFormated.append(camera.id + ":" + camera.name)

#Config file
config = configparser.ConfigParser()
createConfig(config)
checkConfig(config)
config.read('./config.ini')

#craete dirs
creatFolders()

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

#set default camera
set_camera(cam_index)

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

aspect_ratio = width/height
zoom_factor = 1

#Build main ui
root = Tk()
root.title("OpenCV Scanner")
bottomFrame = Frame(root)
topFrame = Frame(root)
canvas = Canvas(root)

#setup camera select
selectedCamera = StringVar(topFrame)
for index, camera in enumerate(cameraList):
    if(cam_index == int(camera.id)):
        selectedCamera.set(cameraListFormated[index]) # default value
select = OptionMenu(topFrame, selectedCamera, *cameraListFormated)
select.config(fg='#fff', bg='#313244', highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e", bd=0, activebackground='#424242', activeforeground='#f5c2e7')
select['menu'].config(fg='#fff', bg='#313244', bd=0, activebackground='#424242', activeforeground='#f5c2e7')

config_btn = Button(topFrame, text='⚙', fg='#f5c2e7', bg='#313244', activebackground='#424242', activeforeground='#f5c2e7', highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e", bd=0)

config_btn.pack(side="left")
select.pack(side='left')
    
notification = Label(canvas, fg='#f5c2e7', bg='#313244') 

topFrame.pack(fill="x")
canvas.pack(fill="both", expand=True)
notification.place(x=10,y=10)

#Bind zoom and pan
canvas.bind("<Button>", handle_zoom) 
canvas.bind('<ButtonPress-1>', lambda event: Thread(target=(canvas.scan_mark(event.x, event.y))))
canvas.bind("<B1-Motion>", lambda event: Thread(target=canvas.scan_dragto(event.x, event.y, gain=1)))
root.bind("<Key>",lambda event: handleRotation(controls(vid, event, cut, count, config, notification)))

root.configure(background='#1e1e2e')
canvas.configure(background='#1e1e2e', bd=0, highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e")
topFrame.configure(background='#1e1e2e')

try:
    update()
except:
    messagebox.showerror('Error',"Camera not acessible. Please change the index.")
selectedCamera.trace_add('write', change_camera)

root.mainloop()
vid.release()
