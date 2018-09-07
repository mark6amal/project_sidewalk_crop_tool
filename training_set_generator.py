"""
To obtain the labelData as the CSV
Run getFullLabelList.sql in the Sidewalk Database

"""
import csv
import json
import os
import logging

from PIL import Image, ImageDraw
import math
import shutil

import numpy as np

path_to_label_list = "/Users/marcus/Desktop/labeldata.csv"

gsv_pano_path = "/Volumes/Extreme SSD/Sandbox Data/"

crop_destination_path = "/Users/marcus/Desktop/Training_Data_SVM/Crops_From_4096_2048/"


pano_list = []
label = {
    1 : "CurbRamp",
    2 : "NoCurbRamp",
    3 : "Obstacle",
    4 : "SurfaceProblem",
    5 : "Other",
    6 : "Occlusion",
    7 : "NoSidewalk"
}

crop_height_width = 800 #in Pixels(Default value is: )

pixel_Crop_Size = int((crop_height_width/2)/3.25)

binsize = 25

def bulkExtractCrops(path_to_label_csv, gsv_pano_path, crop_destination_path):
    csv_file = open(path_to_label_csv)
    csv_f = csv.reader(csv_file)

    no_metadata_fail = 0
    no_pano_fail = 0
    counter = 0

    for row in csv_f:
        

        if(len(pano_list) >= binsize * 4):
            break
        pano_id = row[0]
        sv_image_x = float(row[1])
        sv_image_y = float(row[2])
        label_type = int(row[3])
        photographer_heading = float(row[4])
        label_id = int(row[7])

        print("Status: [" + "#" * int(counter/4) + " " * (25 - int(counter/4)) + "]" , end = '\r')
        pano_yaw_deg = 180 - photographer_heading
        x, y = getLabelCoordinates(sv_image_x, sv_image_y, pano_yaw_deg)

        
        pano_img_path = os.path.join(gsv_pano_path, pano_id[:2], pano_id + ".jpg")

       
        
        if os.path.exists(pano_img_path):
            
            if not pano_img_path in pano_list:
                pano = Image.open(pano_img_path)
                if pano.getbbox() == None :
                    continue

                counter += 1
                shutil.copy2(pano_img_path, "/Users/marcus/Desktop/Training_Data_SVM/Pano_4096_2048/")
                pano_list.append(pano_img_path)
            

            
            label_folder = os.path.join(crop_destination_path, label[label_type])
            if not os.path.isdir(label_folder):
                os.makedirs(label_folder)
            destination_folder = os.path.join(label_folder, pano_id[:2])
            if not os.path.isdir(destination_folder):
                os.makedirs(destination_folder)
            crop_name = "{0}_._{1}_._{2}_._{3}_._".format(pano_id, label[label_type], str(x), str(y))
            crop_destination = os.path.join(crop_destination_path, label[label_type], pano_id[:2], crop_name + ".jpg")
            json_destination = os.path.join(crop_destination_path, label[label_type], pano_id[:2], crop_name + ".json")
            if not os.path.exists(crop_destination):
                fixedCropSinglePano(pano_img_path, x, y, crop_destination, label_type)
                createJsonFile(pano_id, x, y, row, json_destination)
                #print("Successfully extracted crop to " + crop_name + ".jpg")
                logging.info(crop_name + ".jpg" + " " + pano_id + " " + str(sv_image_x)
                             + " " + str(sv_image_y) + " " + str(pano_yaw_deg) + " " + str(label_id))
                logging.info("---------------------------------------------------")
        else:
            no_pano_fail += 1
            #print("Panorama image not found.")
            #logging.warn("Skipped label id " + str(label_id) + " due to missing image.")

    print("Finished.")
    print(str(no_pano_fail) + " extractions failed because panorama image was not found.")
    print(str(no_metadata_fail) + " extractions failed because metadata was not found.")




def createJsonFile(panoId, x, y, row, destination):
    #Adds the data into a dictionary
    data = {}
    data["Pano_Data"] = []
    data["Pano_Data"].append({
       'GSV_Pano_ID': panoId,
        'label_x': str(x),
        'label_y': str(y),
        'x1': str(x - pixel_Crop_Size),
        'y1': str(y - pixel_Crop_Size),
        'x2': str(x + pixel_Crop_Size),
        'y2': "{0}".format((y + pixel_Crop_Size)),
        'sv_image_x': row[1],
        'sv_image_y': row[2],
        'label_type': label[int(row[3])],
        'label_type_id': row[3],
        'pano_yaw-deg' : 180 - float(row[4]),
        'photographer_heading': row[4],
        'heading': row[5],
        'pitch': row[6],
        'label_id': row[7]
        
    })
    #Exports the json file to destination folder
    with open(destination, 'w') as outfile:
        json.dump(data, outfile)


def getLabelCoordinates(sv_image_x, sv_image_y, pano_yaw_deg):
    pano_width = 13312
    pano_height = 6656


    x_label = ((float(pano_yaw_deg) / 360) * pano_width + sv_image_x) % pano_width
    y_label = pano_height / 2 - sv_image_y
    return x_label/3.25 , y_label/3.25

def fixedCropSinglePano(pano_img_path, x, y, crop_destination, label_id, tag = False):
    pano = Image.open(pano_img_path)
    tag = Image.open("./Tags/{0}.png".format(label[label_id]))
    x = int(x)
    y = int(y)
    
    croppedPano = pano.crop((x - pixel_Crop_Size, y - pixel_Crop_Size, x + pixel_Crop_Size, y + pixel_Crop_Size))

    # Saves cropped Pano without tag

    croppedPano.save(crop_destination)

    
    # Saves cropped Pano with tag
    if tag:
        croppedPano.paste(tag, (int(croppedPano.height/2 - tag.height/2), int(croppedPano.width/2 - tag.width/2)))
        croppedPano.save(crop_destination[:-4] + "_tagged.jpg")
    


bulkExtractCrops(path_to_label_list, gsv_pano_path, crop_destination_path)
