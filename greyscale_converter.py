# Converts the images to Grey Scale

import os
from PIL import Image

directory = "/Users/marcus/Desktop/Training_Data_SVM/"

for dir_name, sub_dir_list, file_list in os.walk(directory):
    for file_name in file_list:
        if file_name[-4:] == ".jpg" and len(file_name) > 5:
            image_path = os.path.join(dir_name, file_name)
            img = Image.open(image_path)
            img = img.convert('L')
            
            img.save(image_path)

#92SUJnrOHFZibOepVWlvSA_._CurbRamp_._3540.082892628209_._1456.3076923076924_._.jpg