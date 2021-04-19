import os

from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import sys

COLOR = ['red','blue','green'] #Couleurs pour nos segmentations
#path_json = sys.argv[0]
#path_image = sys.argv[1]
path_json = "/home/yfrendo/Data/DATASET MorphoTique/0-Ixodes_masques/test_json.json"
path_image = "/home/yfrendo/Data/DATASET MorphoTique/0-Ixodes"
df_json = pd.read_json(path_json)
df_json = df_json.transpose().reset_index()[['filename','regions']] #On réduit un peu

if not os.path.exists('Masques'):
    os.makedirs('Masques')

for image_id in range(len(df_json['regions'])):
    image = path_image + '/' + df_json['filename'][image_id]
    im = Image.open(image)
    x, y = im.size #Tille de l'image
    font = Image.new('RGB',(x,y),(0, 0, 0)) #Un fond blanc de la meme taille que les images
    draw = ImageDraw.Draw(font) #Pour dessiner nos polygones

    all_poly = [] #Pour ranger tout nos polygones
    for segmentation in range(len(df_json['regions'][image_id])):
        all_x = df_json['regions'][image_id][segmentation]['shape_attributes']['all_points_x'] #Extraction des X
        all_y = df_json['regions'][image_id][segmentation]['shape_attributes']['all_points_y'] #Extraction des Y

        poly = [] #Création de la liste pour créer le polygone

        if len(all_x) != len(all_y): #Une petite vérification
            raise ValueError('Il doit y avoir autant de X que de Y dans le polygone')

        for k in range(len(all_x)):
            poly.append((all_x[k],all_y[k])) #Création des tupples pour le polynome
        
        if list(df_json['regions'][image_id][segmentation]['region_attributes']['Region'].keys())[0] == "Bouclier": #On détermine la couleur en fonction de la segmentation
            col = COLOR[0]
        
        elif list(df_json['regions'][image_id][segmentation]['region_attributes']['Region'].keys())[0] == "Abdomen":
            col = COLOR[1]

        elif list(df_json['regions'][image_id][segmentation]['region_attributes']['Region'].keys())[0] == "Rostre":
            col = COLOR[2]

        all_poly.append((poly,col))
    
    for polygone,couleur in all_poly:
        draw.polygon(xy = polygone,fill= couleur)
    font.save("./Masques/" + df_json['filename'][image_id] + "_masque", "JPEG")


