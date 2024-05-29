import subprocess

class Camera:
  def __init__(self, name, id):
    self.name = name
    self.id = id 

def createCameraList():
    output = subprocess.check_output("ls /dev/ | grep video", shell=True)
    cameraList = output.decode('ascii').split('\n')

    cameraInfo = []
    cameraInfoName = []
    for camera in cameraList:
        if(camera != ''):
            temp = subprocess.check_output("v4l2-ctl -d /dev/" + camera+ " --info", shell=True)
            start = temp.decode('ascii').split('Name')
            temp = start[1].split('\n')[0].split(':')[1]
            cameraInfo.append(temp)

    for index, camera in enumerate(cameraList):
        if(camera != ''):
            temp = Camera(cameraInfo[index], camera.replace('video',''))
            cameraInfoName.append(temp)

    return cameraInfoName
