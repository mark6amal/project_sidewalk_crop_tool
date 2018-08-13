"""
To obtain the labelData as the CSV 
Run getFullLabelList.sql in the Sidewalk Database

"""

"""
        'sv_image_x':
        'sv_image_y':
        'label_type':
        'label_type_id':
        'photographer_heading':
        'heading':
        'pitch':
        'label_id':
        """

import json

"""
path_to_label_list = 

gsv_pano_path =

crop_destination_path = 

"""

crop_height_width = 100 #in Pixels(Default value is: )

pixel_Crop_Size = crop_height_width/2


def createJsonFile(panoId, x, y):
    data = {}
    data["Pano_Data"] = []
    data["Pano_Data"].append({
       'GSV_Pano_ID': panoId,
        # (x,y) coordinates of the label relative to fullsize pano
        'label_x': str(x),
        'label_y': str(y),
        'x1': str(x - pixel_Crop_Size),
        'y1': str(y - pixel_Crop_Size),
        'x2': str(x + pixel_Crop_Size),
        'y2': "{0}".format((y + pixel_Crop_Size))
    })

    with open(panoId + ".json", 'w') as outfile:
        json.dump(data, outfile, indent = 4)


#def saveCropPano(x, y, panoId)






def getLabelCoordinates(sv_image_x, sv_image_y, photographer_heading):
    pano_width = 13312
    pano_height = 6656

    PanoYawDeg = 180 - photographer_heading

    x_label = ((float(PanoYawDeg) / 360) * pano_width + sv_image_x) % pano_width
    y_label = pano_height / 2 - sv_image_y
    return x_label, y_label





#def bulkExtractCrops(path_to_label_list, gsv_pano_path, crop_destination_path)


createJsonFile("this is a test pano id", 400, 500)