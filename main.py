#!/usr/bin/env python3
# pylint: disable=unused-variable

from Ptera_object import Segmentation
from tqdm import tqdm #Une petite barre de progression on sait jamais ca peut etre long
import random
import sys

TRANSFO = ["seg.rotate_90()","seg.rotate_180()","seg.rotate_270()","seg.flip_LR()","seg.flip_TB()","seg.contrast(","seg.sharp(","seg.gaussian_noise()"] #Liste des transfos possible

def main(path_json,path_image,liste_seg,interet = True, reshape = (512,512),value_augmentation = 0,enregistrement = "."):

    enregistrement = str(enregistrement)

    if value_augmentation < 0 or value_augmentation > len(TRANSFO) + 1:
        raise ValueError ("value_augmentation doit etre compris entre 0 et " + str(len(TRANSFO)+1))

    seg = Segmentation(path_json,path_image,liste_seg,reshape,enregistrement=enregistrement)

    for image_id in tqdm(range(len(seg.df_json['regions']))):
        seg.prep_image(image_id)

        if interet == True: #Cas ou on isole la zone d'interet

            for segmentation in range(len(seg.df_json['regions'][image_id])):
                if "Interet" not in seg.df_json['regions'][image_id][segmentation]['region_attributes'] and interet == True:
                    raise ValueError("'Interet' n'est pas dans la liste des attribute,si vous ne voulez pas découper la régions d'intéret veuillez mettre interet = False")

                if list(seg.df_json['regions'][image_id][segmentation]['region_attributes']['Interet'].keys())[0] == "non":
                    seg.create_polygon(image_id,segmentation)
                else:
                    seg.create_interet(image_id,segmentation)

            seg.segmentation_image()
            seg.decoupe_interet()
            seg.resize_image()
            seg.save(enregistrement)

            if value_augmentation != 0:

                transfo_restante = list(TRANSFO) #On prend les transfo possible
                random.shuffle(transfo_restante) #On mélange

                for k in range(value_augmentation - 1): #Pour que le coefiscient multiplicateur sois bien le bon
                    transfo = transfo_restante.pop() #Supprime et renvoie le dernier élément de la lsite

                    if transfo == "seg.contrast(": #Permet de rajouter de l'aléatoire dans le constrasste et le sharp
                        strength = round(random.choice([0.5,1.3]) + random.uniform(0,0.2),3)
                        transfo = transfo + str(strength) + ')'
                        exec(transfo)
                    elif transfo == "seg.sharp(":
                        strength = round(random.uniform(1.7,2),3)
                        transfo = transfo + str(strength) + ')'
                        exec(transfo)
                    else:
                        exec(transfo)
                    seg.save(original = False) #Et on sauvegarde
        
        else: #Autre cas
            for segmentation in range(len(seg.df_json['regions'][image_id])):
                seg.create_polygon(image_id,segmentation)
            seg.segmentation_image()
            seg.resize_image()
            seg.save(enregistrement)

if __name__ == "__main__":

    script = "main(path_json,path_image,liste_seg"
    path_json = sys.argv[1]
    path_image = sys.argv[2]
    liste_seg = sys.argv[3]

    if "-s" in sys.argv:
        reshape = sys.argv[sys.argv.index('-s') + 1].split(",")
        reshape = (reshape[0],reshape[1])
        script = script + ',reshape = reshape'

    if "-A" in sys.argv:
        augmentation = int(sys.argv[sys.argv.index('-A') + 1])
        script = script + ',value_augmentation = augmentation'
    
    if "-E" in sys.argv:
        path_enregistrement = sys.argv[sys.argv.index('-E') + 1]
        script = script + ',enregistrement = path_enregistrement'
    
    if "-c" in sys.argv:
        script = script + ',interet = False'
    
    print(script)

    exec(script + ')')