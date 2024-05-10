import os
import configparser

def createConfig(config):
    if(os.path.isfile("./config.ini") == False):
        print("No config file detected. Creating one with default configs.")
        config['camera_default'] = {
            'os': 'linux',
            'cam_index':'0',
            'focus':'400.0',
            'contrast':'64.0',
            'saturation': '30',
            'rotation': '270',
            'fps': '60.0',
            'width':  '2048',
            'height': '1536'
        }
        config['controls'] = {
            'toggleAutoExposure':'e',
            'toggleAutoFocus':'f',
            'exposure-':'u',
            'exposure+':'i',
            'brightness-':'o',
            'brightness+':'p',
            'focus-':'[',
            'focus+':']',
            'gain-':'j',
            'gain+':'k',
            'contrast-':'l',
            'contrast+':';',
            'rotate-90':',',
            'rotate+90':'.',
            'addPage':'92',
            'saveFile':'103'
        }
        config.write(open('config.ini', 'w'))

def creatFolders():
    if(os.path.isdir('./.temp') == False):
        os.mkdir('./.temp')
    if(os.path.isdir('./pdf_output') == False):
        os.mkdir('./pdf_output')

def checkConfig(config):
    if(os.path.isfile("./config.ini") == True):
        config.read_file(open('./config.ini'))
        try:
            config.get('camera_default', 'os')
            config.get('camera_default', 'cam_index')
            config.get('camera_default', 'focus')
            config.get('camera_default', 'contrast')
            config.get('camera_default', 'saturation')
            config.get('camera_default', 'rotation')
            config.get('camera_default', 'width')
            config.get('camera_default', 'height')
            config.get('camera_default', 'fps')

            config.get('controls', 'toggleAutoExposure')
            config.get('controls', 'toggleAutoFocus')
            config.get('controls', 'exposure-')
            config.get('controls', 'exposure+')
            config.get('controls', 'brightness-')
            config.get('controls', 'brightness+')
            config.get('controls', 'focus-')
            config.get('controls', 'focus+')
            config.get('controls', 'gain-')
            config.get('controls', 'gain+')
            config.get('controls', 'contrast-')
            config.get('controls', 'contrast+')
            config.get('controls', 'rotate-90')
            config.get('controls', 'rotate+90')
            config.get('controls', 'addPage')
            config.get('controls', 'saveFile')

        except configparser.NoOptionError:
            if input("Config file corrupted. Create new one? ") == 'y' or 'Y' :
                os.remove('./config.ini')
                createConfig(config)
 
            

