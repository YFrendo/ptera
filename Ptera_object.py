import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import pandas as pd
import numpy as np
import sys
import random
from transfo_func import noise_generator

class Segmentation:

    def __init__(self,path_json,path_image,liste_seg,reshape):

        self.df_json = pd.read_json(path_json) #On importe le data set
        self.df_json = self.df_json.transpose().reset_index()[['filename','regions']]

        self.path_image = path_image
        self.liste_seg = liste_seg

        self.im = None #ON définis nos attribut pour la suite
        self.font = None
        self.draw = None
        self.im_transfo = None
        self.font_transfo = None

        self.x_crop = None
        self.y_crop = None
        self.width_crop = None
        self.height_crop = None

        self.all_poly = [] #Pour ranger les polygones

        self.COLOR = ['red','blue','yellow','green','pink'] #Nos couleurs de segmentations
        self.id_save = 0 #On initialise le nombre de fichiers sauvegardé

        if type(self.liste_seg) != list:
            raise TypeError("La liste des segmentation doit etre une liste!")
        
        try:
            self.width, self.height = reshape #Taille des fichiers voulu
            self.width = int(self.width)
            self.height = int(self.height)
        except:
            raise ValueError("reshape doit etre un tupple (width,height)")
        
        if (self.width or self.height) <= 0:
            raise ValueError("reshape doit contenir des entiers positifs")

        if not os.path.exists('Masques'): #On fait les dossier de sauvegarde des sorties
            os.makedirs('Masques')
        if not os.path.exists('Images'):
            os.makedirs('Images')

    def prep_image(self,image_id):
        """Importe une image et créer les objet nécéssaire"""

        self.all_poly = [] #Faut le vider a chaque image!
        image = self.path_image  + self.df_json['filename'][image_id]
        self.im = Image.open(image)
        x, y = self.im.size #Tille de l'image
        self.font = Image.new('RGB',(x,y),(0, 0, 0)) #Un fond noir de la meme taille que les images
        self.draw = ImageDraw.Draw(self.font) #Pour dessiner nos polygones
    
    def create_polygon(self,image_id,segmentation):

        """Exrtrait le polygone pour une segmentation et le stocke dans self.all_poly"""
        

        try:
            self.df_json['regions'][image_id][segmentation]['region_attributes']['Segmentation']
            pass
        except:
            raise ValueError('Il doit y avoir un attribut Segmentation')

        try:
            all_x = self.df_json['regions'][image_id][segmentation]['shape_attributes']['all_points_x'] #Extraction des X
            all_y = self.df_json['regions'][image_id][segmentation]['shape_attributes']['all_points_y'] #Extraction des Y
        except:
            raise ValueError('PTERA ne supporte que les polygones pour la segmentation')

        poly = [] #Création de la liste pour créer le polygone

        if len(all_x) != len(all_y): #Une petite vérification
            raise ValueError('Il doit y avoir autant de X que de Y dans le polygone!')
        
        for k in range(len(all_x)):
            poly.append((all_x[k],all_y[k])) #Création des tupples pour le polynome

        attribut = list(self.df_json['regions'][image_id][segmentation]['region_attributes']['Segmentation'].keys())

        if not all(item in self.liste_seg for item in attribut) : #Si il y a des éléments en plus il ne seront pas segmenté (aucune erreur)
            raise ValueError ('liste_seg doit comprendre tout les éléments segmenté')
        
        for k in range(len(self.liste_seg)):
            if list(self.df_json['regions'][image_id][segmentation]['region_attributes']['Segmentation'].keys())[0] == self.liste_seg[k]:
                col = self.COLOR[k]

        self.all_poly.append((poly,col))
    
    def create_interet(self,image_id,segmentation):

        """S'occupe de faire la découpe pour la zone d'interet"""

        self.x_crop = self.df_json['regions'][image_id][segmentation]['shape_attributes']['x']
        self.y_crop = self.df_json['regions'][image_id][segmentation]['shape_attributes']['y']
        self.width_crop = self.df_json['regions'][image_id][segmentation]['shape_attributes']['width']
        self.height_crop = self.df_json['regions'][image_id][segmentation]['shape_attributes']['height']
    
    def segmentation_image(self):

        """Va faire la segmentation"""

        for polygone,couleur in self.all_poly:
                self.draw.polygon(xy = polygone,fill= couleur)
    
    def decoupe_interet(self): 

        """Decoupe la zone d'interet"""

        self.im = self.im.crop((self.x_crop,self.y_crop,self.x_crop + self.width_crop, self.y_crop + self.height_crop)) #Découpe zone interet
        self.font = self.font.crop((self.x_crop,self.y_crop,self.x_crop + self.width_crop, self.y_crop + self.height_crop))
    
    def resize_image(self):

        """Resize l'image"""

        self.im = self.im.resize((self.width,self.height),Image.LANCZOS) #Reshape
        self.font = self.font.resize((self.width,self.height),Image.LANCZOS)

    def save(self, original = True):

        """Sauvegarde l'image et le fond, mettre original = False si on veut enregistrer les modifications"""

        if original:
            self.font.save("./Masques/" + str(self.id_save).zfill(6) + ".png", "PNG") #Sauvegarde
            self.im.save("./Images/" + str(self.id_save).zfill(6) + ".png", 'PNG')
            self.id_save += 1 #Une image de plus  
        else:
            self.font_transfo.save("./Masques/" + str(self.id_save).zfill(6) + ".png", "PNG") #Sauvegarde
            self.im_transfo.save("./Images/" + str(self.id_save).zfill(6) + ".png", 'PNG')
            self.id_save += 1 #Une image de plus              

    
    def rotate_90(self):

        """Fait tourner l'image de 90°"""

        self.im_transfo = self.im.transpose(method=Image.ROTATE_90)
        self.font_transfo = self.font.transpose(method=Image.ROTATE_90)

    def rotate_180(self):

        """Fait tourner l'image de 180°"""

        self.im_transfo = self.im.transpose(method=Image.ROTATE_180)
        self.font_transfo = self.font.transpose(method=Image.ROTATE_180)

    def rotate_270(self):

        """Fait tourner l'image de 270°"""

        self.im_transfo = self.im.transpose(method=Image.ROTATE_270)
        self.font_transfo = self.font.transpose(method=Image.ROTATE_270)

    def flip_LR(self):

        """FLIP l'image de gauche à droite"""

        self.im_transfo = self.im.transpose(method=Image.FLIP_LEFT_RIGHT)
        self.font_transfo = self.font.transpose(method=Image.FLIP_LEFT_RIGHT)

    def flip_TB(self):

        """FLIP l'image de haut en bas"""

        self.im_transfo = self.im.transpose(method=Image.FLIP_TOP_BOTTOM)
        self.font_transfo = self.font.transpose(method=Image.FLIP_TOP_BOTTOM)
    
    def contrast(self,strength = 1.5):

        """Rajoute du contraste"""

        enhancer = ImageEnhance.Contrast(self.im) #Contraste
        self.im_transfo = enhancer.enhance(strength) #Application que sur l'image!
        self.font_transfo = self.font
    
    def sharp(self,strength = 2):

        """Augmente les contours"""

        enhancer = ImageEnhance.Sharpness(self.im) #Sharp
        self.im_transfo = enhancer.enhance(strength)#Application que sur l'image!
        self.font_transfo = self.font

    def gaussian_noise(self,type = 's&p'):

        """
        Rajoute du bruit à l'image:

            'gauss'        Gaussian-distrituion based noise
            'poission'     Poission-distribution based noise
            's&p'          Salt and Pepper noise, 0 or 1
            'speckle'      Multiplicative noise using out = image + n*image
                           where n is uniform noise with specified mean & variance
        """

        self.im_transfo = noise_generator(type,np.array(self.im)) #Gauss a pas l'air de marcher ca sera donc s&p
        self.im_transfo = Image.fromarray(self.im_transfo, 'RGB')
        self.font_transfo = self.font

        






        

                
    


    


