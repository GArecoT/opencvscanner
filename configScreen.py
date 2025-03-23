from tkinter import (
    messagebox,
    Tk,
    Canvas,
    Button,
    Frame,
    Label,
    OptionMenu,
    StringVar,
    Entry,
)
import configparser
from listCamera import createCameraList


# TODO: List and parse resolutions


def handleRemap(event, root, value, config, item):
    value.config(
        text=event.keysym,
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
    )
    config.set("controls", item, event.keysym)
    root.unbind("<Key>")
    return value


def handleInput(root, value, config, item):
    value.config(
        activebackground="#f5c2e7",
        activeforeground="#000",
        bg="#f5c2e7",
        fg="#000",
    )
    root.bind("<Key>", lambda event: handleRemap(event, root, value, config, item))


def save(
    root,
    config,
    selectedOs,
    selectedCamera,
    focusValue,
    contrastValue,
    saturationValue,
    selectedRotation,
):
    config.set("camera_default", "os", str(selectedOs.get()).lower())
    config.set("camera_default", "cam_index", str(selectedCamera.get()).split(":")[0])
    config.set("camera_default", "focus", str(focusValue.get()))
    config.set("camera_default", "contrast", str(contrastValue.get()))
    config.set("camera_default", "saturation", str(saturationValue.get()))
    config.set("camera_default", "rotation", str(selectedRotation.get()))
    config.write(open("config.ini", "w"))
    messagebox.showerror("Warning", "Restart the program to apply changes")
    root.destroy()


def spawnConfig():
    config = configparser.ConfigParser()
    config.read("./config.ini")

    osOptions = ["Windows", "Linux"]
    rotationOptions = ["0", "90", "180", "270"]

    # list cameras
    cameraList = createCameraList()
    cameraOptions = []

    for camera in cameraList:
        cameraOptions.append(camera.id + ":" + camera.name)

    root = Tk()
    root.title("OpenCV Scanner settings")
    root.configure(background="#1e1e2e")

    # Label
    label = Label(root, text="Settings", fg="#f5c2e7", bg="#1e1e2e", font=("Noto", 25))
    labelMain = Label(
        root, text="Main settings", fg="#f5c2e7", bg="#1e1e2e", font=("Noto", 15)
    )
    labelCamera = Label(
        root, text="Camera settings", fg="#f5c2e7", bg="#1e1e2e", font=("Noto", 15)
    )
    labelShortcuts = Label(
        root, text="Shortcuts", fg="#f5c2e7", bg="#1e1e2e", font=("Noto", 15)
    )

    # Config canvas
    canvas1 = Canvas(root)
    canvas1.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    canvas2 = Canvas(root)
    canvas2.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    canvas3 = Canvas(root)
    canvas3.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    canvas4 = Canvas(root)
    canvas4.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    canvas5 = Canvas(root)
    canvas5.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    canvasControls = Canvas(root)
    canvasControls.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )

    # OS Select
    osSelectCanvas = Canvas(canvas1)
    osSelectCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    selectedOs = StringVar(osSelectCanvas)
    # Set configs
    if config.get("camera_default", "os") == "windows":
        selectedOs.set(osOptions[0])
    elif config.get("camera_default", "os") == "linux":
        selectedOs.set(osOptions[1])
    selectOS = OptionMenu(osSelectCanvas, selectedOs, *osOptions)
    selectOS.config(
        fg="#fff",
        bg="#313244",
        highlightbackground="#1e1e2e",
        bd=0,
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightcolor="#f5c2e7",
    )
    selectOS["menu"].config(
        fg="#fff",
        bg="#313244",
        bd=0,
        activebackground="#424242",
        activeforeground="#f5c2e7",
    )
    labelOsSelect = Label(osSelectCanvas, text="OS", fg="#fff", bg="#1e1e2e")
    labelOsSelect.pack()
    selectOS.pack()

    # Camera Select
    cameraSelectCanvas = Canvas(canvas1)
    cameraSelectCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    selectedCamera = StringVar(cameraSelectCanvas)
    for index, camera in enumerate(cameraList):
        if int(config.get("camera_default", "cam_index")) == int(camera.id):
            selectedCamera.set(cameraOptions[index])  # de# default value
    selectCamera = OptionMenu(cameraSelectCanvas, selectedCamera, *cameraOptions)
    selectCamera.config(
        fg="#fff",
        bg="#313244",
        highlightbackground="#1e1e2e",
        bd=0,
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightcolor="#f5c2e7",
    )
    selectCamera["menu"].config(
        fg="#fff",
        bg="#313244",
        bd=0,
        activebackground="#424242",
        activeforeground="#f5c2e7",
    )
    labelCameraSelect = Label(
        cameraSelectCanvas, text="Default camera", fg="#fff", bg="#1e1e2e"
    )
    labelCameraSelect.pack()
    selectCamera.pack()

    # Focus Entry
    focusEntryCanvas = Canvas(canvas2)
    focusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    focusValue = StringVar(focusEntryCanvas, str(config.get("camera_default", "focus")))

    labelFocus = Label(
        focusEntryCanvas,
        text="Focus",
        fg="#fff",
        bg="#1e1e2e",
        anchor="w",
        justify="left",
    )
    labelFocus.pack(fill="x")
    entryFocus = Entry(focusEntryCanvas, textvariable=focusValue)
    entryFocus.configure(
        background="#313244",
        bd=0,
        highlightbackground="#313244",
        highlightcolor="#f5c2e7",
        fg="#fff",
        foreground="#fff",
        insertbackground="#fff",
    )
    entryFocus.pack()

    # Contrast Entry
    contrastEntryCanvas = Canvas(canvas2)
    contrastEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    contrastValue = StringVar(
        focusEntryCanvas, str(config.get("camera_default", "contrast"))
    )

    labelContrast = Label(
        contrastEntryCanvas,
        text="Contrast",
        fg="#fff",
        bg="#1e1e2e",
        anchor="w",
        justify="left",
    )
    labelContrast.pack(fill="x")
    entryContrast = Entry(contrastEntryCanvas, textvariable=contrastValue)
    entryContrast.configure(
        background="#313244",
        bd=0,
        highlightbackground="#313244",
        highlightcolor="#f5c2e7",
        fg="#fff",
        foreground="#fff",
        insertbackground="#fff",
    )
    entryContrast.pack()

    # Saturation Entry
    saturationEntryCanvas = Canvas(canvas2)
    saturationEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    saturationValue = StringVar(
        focusEntryCanvas, str(config.get("camera_default", "saturation"))
    )

    labelSaturation = Label(
        saturationEntryCanvas,
        text="Saturation",
        fg="#fff",
        bg="#1e1e2e",
        anchor="w",
        justify="left",
    )
    labelSaturation.pack(fill="x")
    entrySaturation = Entry(saturationEntryCanvas, textvariable=saturationValue)
    entrySaturation.configure(
        background="#313244",
        bd=0,
        highlightbackground="#313244",
        highlightcolor="#f5c2e7",
        fg="#fff",
        foreground="#fff",
        insertbackground="#fff",
    )
    entrySaturation.pack()

    # Rotation Select
    rotationSelectCanvas = Canvas(canvas2)
    rotationSelectCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    selectedRotation = StringVar(rotationSelectCanvas)
    # Set configs
    for index, rotation in enumerate(rotationOptions):
        if config.get("camera_default", "rotation") == rotation:
            selectedRotation.set(rotationOptions[index])
    selectRotation = OptionMenu(
        rotationSelectCanvas, selectedRotation, *rotationOptions
    )
    selectRotation.config(
        fg="#fff",
        bg="#313244",
        highlightbackground="#1e1e2e",
        bd=0,
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightcolor="#f5c2e7",
    )
    selectRotation["menu"].config(
        fg="#fff",
        bg="#313244",
        bd=0,
        activebackground="#424242",
        activeforeground="#f5c2e7",
    )
    labelRotationSelect = Label(
        rotationSelectCanvas, text="Rotation", fg="#fff", bg="#1e1e2e"
    )
    labelRotationSelect.pack()
    selectRotation.pack()

    # exposition
    expositionEntryCanvas = Canvas(canvas3)
    expositionEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelExpositionBtn = Label(
        expositionEntryCanvas, text="Toggle Auto Exposure", fg="#fff", bg="#1e1e2e"
    )
    exposition_btn = Button(
        expositionEntryCanvas,
        text=str(config.get("controls", "toggleAutoExposure")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    exposition_btn.config(
        command=lambda: handleInput(root, exposition_btn, config, "toggleautoexposure"),
    )
    labelExpositionBtn.pack()
    exposition_btn.pack(side="left")

    # focus
    autoFocusEntryCanvas = Canvas(canvas3)
    autoFocusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelFocusBtn = Label(
        autoFocusEntryCanvas, text="Toggle Auto Focus", fg="#fff", bg="#1e1e2e"
    )
    focus_btn = Button(
        autoFocusEntryCanvas,
        text=str(config.get("controls", "toggleAutoFocus")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    focus_btn.config(
        command=lambda: handleInput(root, focus_btn, config, "toggleautofocus"),
    )
    labelFocusBtn.pack()
    focus_btn.pack(side="left")

    # exposure-
    exposureMinusEntryCanvas = Canvas(canvas3)
    exposureMinusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelExposureMinusBtn = Label(
        exposureMinusEntryCanvas, text="Exposure -", fg="#fff", bg="#1e1e2e"
    )
    exposureMinus_btn = Button(
        exposureMinusEntryCanvas,
        text=str(config.get("controls", "exposure-")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    exposureMinus_btn.config(
        command=lambda: handleInput(root, exposureMinus_btn, config, "exposure-"),
    )
    labelExposureMinusBtn.pack()
    exposureMinus_btn.pack(side="left")

    # exposure+
    exposurePlusEntryCanvas = Canvas(canvas3)
    exposurePlusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelExposurePlusBtn = Label(
        exposurePlusEntryCanvas, text="Exposure +", fg="#fff", bg="#1e1e2e"
    )
    exposurePlus_btn = Button(
        exposurePlusEntryCanvas,
        text=str(config.get("controls", "exposure+")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    exposurePlus_btn.config(
        command=lambda: handleInput(root, exposurePlus_btn, config, "exposure+"),
    )
    labelExposurePlusBtn.pack()
    exposurePlus_btn.pack(side="left")

    # brightness-
    brightnessMinusEntryCanvas = Canvas(canvas3)
    brightnessMinusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelBrightnessMinusBtn = Label(
        brightnessMinusEntryCanvas, text="Brightness -", fg="#fff", bg="#1e1e2e"
    )
    brightnessMinus_btn = Button(
        brightnessMinusEntryCanvas,
        text=str(config.get("controls", "brightness-")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    brightnessMinus_btn.config(
        command=lambda: handleInput(root, brightnessMinus_btn, config, "brightness-"),
    )
    labelBrightnessMinusBtn.pack()
    brightnessMinus_btn.pack(side="left")

    # brightness+
    brightnessPlusEntryCanvas = Canvas(canvas3)
    brightnessPlusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelBrightnessPlusBtn = Label(
        brightnessPlusEntryCanvas, text="Brightness +", fg="#fff", bg="#1e1e2e"
    )
    brightnessPlus_btn = Button(
        brightnessPlusEntryCanvas,
        text=str(config.get("controls", "brightness+")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    brightnessPlus_btn.config(
        command=lambda: handleInput(root, brightnessPlus_btn, config, "brightness+"),
    )
    labelBrightnessPlusBtn.pack()
    brightnessPlus_btn.pack(side="left")

    # focus-
    focusMinusEntryCanvas = Canvas(canvas4)
    focusMinusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelFocusMinusBtn = Label(
        focusMinusEntryCanvas, text="Focus -", fg="#fff", bg="#1e1e2e"
    )
    focusMinus_btn = Button(
        focusMinusEntryCanvas,
        text=str(config.get("controls", "focus-")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    focusMinus_btn.config(
        command=lambda: handleInput(root, focusMinus_btn, config, "focus-"),
    )
    labelFocusMinusBtn.pack()
    focusMinus_btn.pack(side="left")

    # Focus+
    focusPlusEntryCanvas = Canvas(canvas4)
    focusPlusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelFocusPlusBtn = Label(
        focusPlusEntryCanvas, text="Focus +", fg="#fff", bg="#1e1e2e"
    )
    focusPlus_btn = Button(
        focusPlusEntryCanvas,
        text=str(config.get("controls", "focus+")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    focusPlus_btn.config(
        command=lambda: handleInput(root, focusPlus_btn, config, "focus+"),
    )
    labelFocusPlusBtn.pack()
    focusPlus_btn.pack(side="left")

    # gain-
    gainMinusEntryCanvas = Canvas(canvas4)
    gainMinusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelGainMinusBtn = Label(
        gainMinusEntryCanvas, text="Gain -", fg="#fff", bg="#1e1e2e"
    )
    gainMinus_btn = Button(
        gainMinusEntryCanvas,
        text=str(config.get("controls", "gain-")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    gainMinus_btn.config(
        command=lambda: handleInput(root, gainMinus_btn, config, "gain-"),
    )
    labelGainMinusBtn.pack()
    gainMinus_btn.pack(side="left")

    # gain+
    gainPlusEntryCanvas = Canvas(canvas4)
    gainPlusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelGainPlusBtn = Label(
        gainPlusEntryCanvas, text="Gain +", fg="#fff", bg="#1e1e2e"
    )
    gainPlus_btn = Button(
        gainPlusEntryCanvas,
        text=str(config.get("controls", "gain+")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    gainPlus_btn.config(
        command=lambda: handleInput(root, gainPlus_btn, config, "gain+"),
    )
    labelGainPlusBtn.pack()
    gainPlus_btn.pack(side="left")

    # contrast-
    contrastMinusEntryCanvas = Canvas(canvas4)
    contrastMinusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelContrastMinusBtn = Label(
        contrastMinusEntryCanvas, text="Contrast -", fg="#fff", bg="#1e1e2e"
    )
    contrastMinus_btn = Button(
        contrastMinusEntryCanvas,
        text=str(config.get("controls", "contrast-")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    contrastMinus_btn.config(
        command=lambda: handleInput(root, contrastMinus_btn, config, "contrast-"),
    )
    labelContrastMinusBtn.pack()
    contrastMinus_btn.pack(side="left")

    # contrast+
    contrastPlusEntryCanvas = Canvas(canvas4)
    contrastPlusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelContrastPlusBtn = Label(
        contrastPlusEntryCanvas, text="Contrast +", fg="#fff", bg="#1e1e2e"
    )
    contrastPlus_btn = Button(
        contrastPlusEntryCanvas,
        text=str(config.get("controls", "contrast+")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    contrastPlus_btn.config(
        command=lambda: handleInput(root, contrastPlus_btn, config, "contrast+"),
    )
    labelContrastPlusBtn.pack()
    contrastPlus_btn.pack(side="left")

    # rotate-90
    rotateMinusEntryCanvas = Canvas(canvas4)
    rotateMinusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelRotateMinusBtn = Label(
        rotateMinusEntryCanvas, text="Rotate -90", fg="#fff", bg="#1e1e2e"
    )
    rotateMinus_btn = Button(
        rotateMinusEntryCanvas,
        text=str(config.get("controls", "rotate-90")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    rotateMinus_btn.config(
        command=lambda: handleInput(root, rotateMinus_btn, config, "rotate-90"),
    )
    labelRotateMinusBtn.pack()
    rotateMinus_btn.pack(side="left")

    # rotate+90
    rotatePlusEntryCanvas = Canvas(canvas4)
    rotatePlusEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelRotatePlusBtn = Label(
        rotatePlusEntryCanvas, text="Rotate +90", fg="#fff", bg="#1e1e2e"
    )
    rotatePlus_btn = Button(
        rotatePlusEntryCanvas,
        text=str(config.get("controls", "rotate+90")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    rotatePlus_btn.config(
        command=lambda: handleInput(root, rotatePlus_btn, config, "rotate+90"),
    )
    labelRotatePlusBtn.pack()
    rotatePlus_btn.pack(side="left")

    # redoPage
    redoPageEntryCanvas = Canvas(canvas5)
    redoPageEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelRedoPageBtn = Label(
        redoPageEntryCanvas, text="Redo Page", fg="#fff", bg="#1e1e2e"
    )
    redoPage_btn = Button(
        redoPageEntryCanvas,
        text=str(config.get("controls", "redoPage")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    redoPage_btn.config(
        command=lambda: handleInput(root, redoPage_btn, config, "redoPage"),
    )
    labelRedoPageBtn.pack()
    redoPage_btn.pack(side="left")

    # AddPage
    addPageEntryCanvas = Canvas(canvas5)
    addPageEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelAddPageBtn = Label(
        addPageEntryCanvas, text="Add Page", fg="#fff", bg="#1e1e2e"
    )
    addPage_btn = Button(
        addPageEntryCanvas,
        text=str(config.get("controls", "addPage")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    addPage_btn.config(
        command=lambda: handleInput(root, addPage_btn, config, "addPage"),
    )
    labelAddPageBtn.pack()
    addPage_btn.pack(side="left")

    # Save File
    saveFileEntryCanvas = Canvas(canvas5)
    saveFileEntryCanvas.configure(
        background="#1e1e2e",
        bd=0,
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
    )
    labelSaveFileBtn = Label(
        saveFileEntryCanvas, text="Add Page", fg="#fff", bg="#1e1e2e"
    )
    saveFile_btn = Button(
        saveFileEntryCanvas,
        text=str(config.get("controls", "saveFile")),
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        anchor="w",
    )
    saveFile_btn.config(
        command=lambda: handleInput(root, saveFile_btn, config, "saveFile"),
    )
    labelSaveFileBtn.pack()
    saveFile_btn.pack(side="left")

    # save cancel buttons
    save_btn = Button(
        canvasControls,
        text="Save",
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        command=lambda: save(
            root,
            config,
            selectedOs,
            selectedCamera,
            focusValue,
            contrastValue,
            saturationValue,
            selectedRotation,
        ),
    )
    cancel_btn = Button(
        canvasControls,
        text="Cancel",
        fg="#f5c2e7",
        bg="#313244",
        activebackground="#424242",
        activeforeground="#f5c2e7",
        highlightbackground="#1e1e2e",
        highlightcolor="#1e1e2e",
        bd=0,
        command=root.destroy,
    )

    # Build main layout
    label.pack(side="top", ipady=10)
    labelMain.pack(side="top", anchor="w", ipadx=10)
    osSelectCanvas.pack(side="left")
    cameraSelectCanvas.pack(side="left")
    canvas1.pack(fill="x", side="top", pady=10, padx=10)
    labelCamera.pack(side="top", anchor="w", ipadx=10, ipady=20)
    focusEntryCanvas.pack(side="left")
    contrastEntryCanvas.pack(side="left", padx=5)
    saturationEntryCanvas.pack(side="left")
    rotationSelectCanvas.pack(side="left", padx=5)
    canvas2.pack(fill="x", side="top", pady=10, padx=10)
    labelShortcuts.pack(side="top", anchor="w", ipadx=10, ipady=20)
    expositionEntryCanvas.pack(side="left")
    exposureMinusEntryCanvas.pack(side="left", padx=20)
    exposurePlusEntryCanvas.pack(side="left", padx=20)
    brightnessMinusEntryCanvas.pack(side="left", padx=20)
    brightnessPlusEntryCanvas.pack(side="left", padx=20)
    autoFocusEntryCanvas.pack(side="left")
    canvas3.pack(fill="x", side="top", pady=10, padx=10)
    focusMinusEntryCanvas.pack(side="left")
    focusPlusEntryCanvas.pack(side="left", padx=20)
    gainMinusEntryCanvas.pack(side="left")
    gainPlusEntryCanvas.pack(side="left", padx=20)
    contrastMinusEntryCanvas.pack(side="left")
    contrastPlusEntryCanvas.pack(side="left", padx=20)
    rotateMinusEntryCanvas.pack(side="left", padx=20)
    rotatePlusEntryCanvas.pack(side="left", padx=20)
    canvas4.pack(fill="x", side="top", pady=10, padx=10)
    redoPageEntryCanvas.pack(side="left")
    addPageEntryCanvas.pack(side="left")
    saveFileEntryCanvas.pack(side="left", padx=20)
    canvas5.pack(fill="x", side="top", pady=10, padx=10)
    save_btn.pack(side="right")
    cancel_btn.pack(side="right")
    canvasControls.pack(fill="x", side="top", pady=10, padx=10)

    root.attributes("-type", "dialog")
    root.mainloop()
