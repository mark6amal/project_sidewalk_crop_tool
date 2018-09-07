import os
from PIL import Image
import shutil

gsv_pano_path = "/Volumes/Samsung_T5/scrapes_dump/"
destination_path = "/Volumes/Extreme SSD/Sandbox Data/"



counter = 0


for dirName, subdirList, fileList in os.walk(gsv_pano_path):
    size = len(os.listdir(gsv_pano_path))
    print("{}/{}".format(counter, size))
    counter += 1

    for fname in fileList:

        filename = fname
        pathName = os.path.join(gsv_pano_path, dirName, fname)
        destinationFolder = os.path.join(destination_path , (dirName[-2:]))
        outputPathName = os.path.join(destination_path, (dirName[-2:]), filename)

        if not os.path.isdir(destinationFolder):
                os.makedirs(destinationFolder)
        
        if not os.path.exists(outputPathName):
    
            if ((fname[-4:] == ".jpg") and (len(fname) > 4)):
                im = Image.open(pathName)
                resized_pano = im.resize((4096, 2048))
                resized_pano.save(outputPathName)
            else:
                shutil.copy2(pathName, outputPathName)
