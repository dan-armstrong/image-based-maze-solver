from PIL import Image
import subprocess

def createThreshold(imageName):
    image = Image.open(imageName).convert('RGB')
    sizeX = image.size[0]
    sizeY = image.size[1]
    pixels = image.load() #PIXEL DATA
    threshold = ''

    for y in range(0,sizeY): #CREATE THRESHOLD GRID FROM IMAGE
        for x in range(0,sizeX):
            if sum(pixels[x,y]) < 255*3*0.5: #IF PIXEL IS DARK
                threshold += '1,'
            else:
                threshold += '0,'
        threshold = threshold[:-1] + '\n'
    return threshold

def findNodes(threshold, scriptPath, csvPath):
    file = open(csvPath, 'w')
    file.write(threshold)
    file.close()

    cmdPath = '/usr/local/bin/Rscript'
    return subprocess.check_output([cmdPath, scriptPath, csvPath], universal_newlines=True).split('\n')
