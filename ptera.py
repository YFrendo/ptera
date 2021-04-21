import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import pandas as pd
import numpy as np
import sys
import random
from tqdm import tqdm #Une petite barre de progression on sait jamais ca peut etre long
from transfo_func import noise_generator

COLOR = ['red','blue','green'] #Couleurs pour nos segmentations

path_json = str(sys.argv[1]) #En premier le chemin vers le JSON
path_image = str(sys.argv[2]) #En deuxième vers les images

id_save = 0 #Pour numéroter nos images

try:
    reshape_width = int(sys.argv[3])
except:
    reshape_width = 512 #Taille par défaut

try:
    reshape_height= int(sys.argv[4])
except:
    reshape_height = 512 #Taille par défaut


#path_json = "/home/yfrendo/Data/DATASET MorphoTique/0-Ixodes_masques/anotation.json"
#path_image = "/home/yfrendo/Data/DATASET MorphoTique/0-Ixodes/"
#test

df_json = pd.read_json(path_json)
df_json = df_json.transpose().reset_index()[['filename','regions']] #On réduit un peu

if not os.path.exists('Masques'): #On fait les dossier de sauvegarde des sorties
    os.makedirs('Masques')
if not os.path.exists('Images'):
    os.makedirs('Images')

for image_id in tqdm(range(len(df_json['regions']))):
    image = path_image  + df_json['filename'][image_id]
    im = Image.open(image)
    x, y = im.size #Tille de l'image
    font = Image.new('RGB',(x,y),(0, 0, 0)) #Un fond noir de la meme taille que les images
    draw = ImageDraw.Draw(font) #Pour dessiner nos polygones

    all_poly = [] #Pour ranger tout nos polygones
    for segmentation in range(len(df_json['regions'][image_id])):

        try: #On vérifie que tout est en place
            df_json['regions'][image_id][segmentation]['region_attributes']['Tique']
            pass
        except:
            raise ValueError('Il doit y avoir un attribut Tique')
        
        try:
            df_json['regions'][image_id][segmentation]['region_attributes']['Region']
            pass
        except:
            raise ValueError('Il doit y avoir un attribut Region')

        if df_json['regions'][image_id][segmentation]['region_attributes']['Tique'] == "non":
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
            else:
                raise ValueError("Les segmentations doivent etre : Bouclier, Abdomen ou Rostre \nValeur de la segmentation = " 
                + str(df_json['regions'][image_id][segmentation]['region_attributes']['Region'].keys())[0]) #Au cas ou quelqun se trompe sur la segmentation

            all_poly.append((poly,col))
        
        else: #Détection de la zone de l'intéret et crop
            x_crop = df_json['regions'][image_id][segmentation]['shape_attributes']['x']
            y_crop = df_json['regions'][image_id][segmentation]['shape_attributes']['y']
            width_crop = df_json['regions'][image_id][segmentation]['shape_attributes']['width']
            height_crop = df_json['regions'][image_id][segmentation]['shape_attributes']['height']

    
    for polygone,couleur in all_poly:
        draw.polygon(xy = polygone,fill= couleur)

    im = im.crop((x_crop,y_crop,x_crop + width_crop, y_crop + height_crop)) #Découpe zone interet
    font = font.crop((x_crop,y_crop,x_crop + width_crop, y_crop + height_crop))

    im = im.resize((reshape_width,reshape_height),Image.LANCZOS) #Reshape
    font = font.resize((reshape_width,reshape_height),Image.LANCZOS)

    font.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") #SAuvegarde
    im.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus

    """On va rajouter un peu d'augmentation"""
    im_transfo = im.transpose(method=Image.ROTATE_90)
    font_transfo = font.transpose(method=Image.ROTATE_90)

    font_transfo.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") #SAuvegarde
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus

    im_transfo = im.transpose(method=Image.ROTATE_180)
    font_transfo = font.transpose(method=Image.ROTATE_180)

    font_transfo.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") #SAuvegarde
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus

    im_transfo = im.transpose(method=Image.ROTATE_270)
    font_transfo = font.transpose(method=Image.ROTATE_270)

    font_transfo.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") #SAuvegarde
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus

    im_transfo = im.transpose(method=Image.FLIP_LEFT_RIGHT)
    font_transfo = font.transpose(method=Image.FLIP_LEFT_RIGHT)

    font_transfo.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") #SAuvegarde
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus

    im_transfo = im.transpose(method=Image.FLIP_TOP_BOTTOM)
    font_transfo = font.transpose(method=Image.FLIP_TOP_BOTTOM)

    font_transfo.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") #SAuvegarde
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus

    enhancer = ImageEnhance.Contrast(im) #Contraste
    im_transfo = enhancer.enhance(0.5) #Application que sur l'image!
    font.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") 
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus

    enhancer = ImageEnhance.Contrast(im) #Contraste
    im_transfo = enhancer.enhance(1.5)#Application que sur l'image!
    font.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") 
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus

    enhancer = ImageEnhance.Sharpness(im) #Sharp
    im_transfo = enhancer.enhance(2)#Application que sur l'image!
    font.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") 
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus


    im_transfo = noise_generator('s&p',np.array(im)) #Gauss a pas l'air de marcher ca sera donc s&p
    im_transfo = Image.fromarray(im_transfo, 'RGB')
    font.save("./Masques/" + str(id_save).zfill(6) + ".png", "PNG") 
    im_transfo.save("./Images/" + str(id_save).zfill(6) + ".png", 'PNG')
    id_save += 1 #Une image de plus







