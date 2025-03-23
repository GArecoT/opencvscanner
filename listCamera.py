import subprocess

class Camera:
  def __init__(self, name, id):
    self.name = name
    self.id = id 

def createCameraList():
    output = subprocess.check_output("v4l2-ctl --list-devices", shell=True)
    tempCameras = output.decode('ascii').split('\n\n')
    cameraInfoName = []
    for tempCamera in tempCameras:
        temp = tempCamera.split('\n\t')
        print(temp)
        if(len(temp) > 1):
            camera = Camera(temp[0], temp[1].replace('/dev/video',''))
            cameraInfoName.append(camera)
    return cameraInfoName
