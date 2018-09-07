import json
import os

"""
    After running the crop_tool.py script and generating the respective folders for the crop/pano destination
    run this script. The purpose of this script is to create a json file in which all of the important label data 
    can be easily stored and access. This script reads all of the label json files, and adds the label_x, label_y,
    label_type, and label_id to a json file that should be located in the pano_location below (named: <pano_id>.json)
"""

# Update file directories HERE

crop_location= "/Users/marcus/Desktop/Training_Data_SVM/Crops_From_4096_2048/"
pano_location = "/Users/marcus/Desktop/Training_Data_SVM/Pano_4096_2048/"

# Are you using resized panoromas? Update it HERE
pano_width = "_" + "4096"  # <---- width
pano_height = "_" + "2048" # <---- height


# Adds all the json files associated with a label/crop to a list
crop_json_list = []
for dir_name, sub_dir_list, file_list in os.walk(crop_location):
    for file_name in file_list:
        if file_name[-5:] == ".json" and len(file_name) > 20:
            crop_json_list.append(file_name)


def create_json_file_with_all_labels():
    for json_file in crop_json_list:
        # Splits the file name into the data that is used to locate Panos, Crops, (x, y), etc
        data = json_file.split('_._')
        
        pano_json_location = os.path.join(pano_location, data[0] + pano_width + pano_height + "_label" + data[4])
        crop_json_location = os.path.join(crop_location, data[1], data[0][:2], json_file)

        # Opens the crop json file for reading
        with open(crop_json_location, 'r') as crop_file:
            crop = json.load(crop_file)
        # Out of Range label_id, will be changed later
        label_id = -1
        for x in crop['Pano_Data']:
            label_id = x['label_id']
        # Creates new json file for the 
        if not os.path.exists(pano_json_location):
            filedata = {}
            filedata[data[0]] = []
            with open(pano_json_location, 'w') as outfile:
                filedata[data[0]].append({
                    'label_id'   : label_id,
                    'label_type' : data[1],
                    'x'          : float(data[2]),
                    'y'          : float(data[3])
                })
                json.dump(filedata, outfile)
        else:
            with open(pano_json_location, 'r') as json_file:
                filedata = json.load(json_file)
            filedata[data[0]].append({
                'label_id'   : label_id,
                'label_type' : data[1],
                'x'          : float(data[2]),
                'y'          : float(data[3])
            })

            with open(pano_json_location, 'w') as json_file:
                json.dump(filedata, json_file)
        
create_json_file_with_all_labels()