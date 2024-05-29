from tkinter import messagebox, Tk, Canvas, Button, Frame, Label, OptionMenu, StringVar, Entry
import configparser
from listCamera import createCameraList

def spawnConfig():
    config = configparser.ConfigParser()
    config.read('./config.ini')

    osOptions = ['Windows', 'Linux']

#list cameras
    cameraList = createCameraList()
    cameraOptions = []

    for camera in cameraList:
        cameraOptions.append(camera.id + ":" + camera.name)

    root = Tk()
    root.title("OpenCV Scanner settings")
    root.configure(background='#1e1e2e')


#Label
    label = Label( root, text="Settings", fg='#f5c2e7', bg='#1e1e2e', font=('Noto', 25))
    labelMain = Label( root, text="Main settings", fg='#f5c2e7', bg='#1e1e2e', font=('Noto', 15))
    labelCamera = Label( root, text="Camera settings", fg='#f5c2e7', bg='#1e1e2e', font=('Noto', 15))

#Config canvas
    canvas = Canvas(root)
    canvas.configure(background='#1e1e2e', bd=0, highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e")

#OS Select
    osSelectCanvas = Canvas(canvas)
    osSelectCanvas.configure(background='#1e1e2e', bd=0, highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e")
    selectedOs = StringVar(osSelectCanvas)
#Set configs
    if(config.get('camera_default', 'os') == 'windows'):
        selectedOs.set(osOptions[0])
    elif(config.get('camera_default', 'os') == 'linux'):
        selectedOs.set(osOptions[1])
    selectOS = OptionMenu(osSelectCanvas, selectedOs, *osOptions)
    selectOS.config(fg='#fff', bg='#313244', highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e", bd=0, activebackground='#424242', activeforeground='#f5c2e7')
    selectOS['menu'].config(fg='#fff', bg='#313244', bd=0, activebackground='#424242', activeforeground='#f5c2e7')
    labelOsSelect = Label( osSelectCanvas, text="OS", fg='#fff', bg='#1e1e2e')
    labelOsSelect.pack()
    selectOS.pack()

#Camera Select
    cameraSelectCanvas = Canvas(canvas)
    cameraSelectCanvas.configure(background='#1e1e2e', bd=0, highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e")
    selectedCamera = StringVar(cameraSelectCanvas)
    for index, camera in enumerate(cameraList):
        if(int(config.get("camera_default", "cam_index")) == int(camera.id)):
            selectedCamera.set(cameraOptions[index]) # de# default value
    selectCamera = OptionMenu(cameraSelectCanvas, selectedCamera, *cameraOptions)
    selectCamera.config(fg='#fff', bg='#313244', highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e", bd=0, activebackground='#424242', activeforeground='#f5c2e7')
    selectCamera['menu'].config(fg='#fff', bg='#313244', bd=0, activebackground='#424242', activeforeground='#f5c2e7')
    labelCameraSelect = Label( cameraSelectCanvas, text="Default camera", fg='#fff', bg='#1e1e2e')
    labelCameraSelect.pack()
    selectCamera.pack()

    #Focus Entry
    focusEntryCanvas = Canvas(canvas)
    focusEntryCanvas.configure(background='#1e1e2e', bd=0, highlightbackground = "#1e1e2e", highlightcolor= "#1e1e2e")
    focusValue = StringVar(focusEntryCanvas)

    entryFocus = Entry(focusEntryCanvas,textvariable=focusValue)
    entryFocus.pack()

#Build main layout
    label.pack(side="top", ipady=10)
    labelMain.pack(side="top", anchor='w', ipadx=10)
    osSelectCanvas.pack(side='left')
    cameraSelectCanvas.pack(side="left")
    canvas.pack(fill="x", side="top", pady=10, padx=10)
    labelCamera.pack(side="top", anchor='w', ipadx=10, ipady=20)
    focusEntryCanvas.pack(side="left")

    root.mainloop()
