import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import pandas as pd
import numpy as np
import sys
import random
from tqdm import tqdm #Une petite barre de progression on sait jamais ca peut etre long
from transfo_func import noise_generator

class Segmentation:

    def __init__(self,path_json,path_image,liste_seg,reshape = (512,512)):
        
        self.path_json = path_json
        self.path_image = path_image
        self.liste_seg = liste_seg

        self.COLOR = ['red','blue','yellow',] #Nos couleurs de segmentations
        self.id_save = 0 #On initialise le nombre de fichiers sauvegardé

        if type(self.liste_seg) != list:
            raise TypeError("La liste des segmentation doit etre une liste!")

        self.width, self.height = reshape #Taille des fichiers voulu

        if not os.path.exists('Masques'): #On fait les dossier de sauvegarde des sorties
            os.makedirs('Masques')
        if not os.path.exists('Images'):
            os.makedirs('Images')


    


