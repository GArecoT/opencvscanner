from tkinter import NW, Tk, Canvas, PhotoImage
import cv2 
from controls import controls
from imageprocess import image_process
from createConfig import createConfig, checkConfig, creatFolders
import configparser

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
    h, w = img.shape[:2]
    data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
    print(w, h)
    return PhotoImage(width=w, height=h, data=data, format='PPM')

def update():
    ret, frame = vid.read()
    frame = cv2.resize(frame, (resize_image()))
    image_copy, cut = image_process(frame, rotation)

    root.bind("<Key>",lambda event: handleRotation(controls(vid, event, cut, count, config)))
    if ret:
        photo = photo_image(image_copy)
        canvas.create_image(canvas.winfo_width()/2, 20, image=photo, anchor='n')
        canvas.image = photo
    root.after(15, update)


#Start Loop
aspect_ratio = 16/9
root = Tk()
root.title("OpenCV Scanner")
canvas = Canvas(root)
canvas.pack(fill="both", expand=True)
update()
root.mainloop()
vid.release()
