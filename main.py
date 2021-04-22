from Ptera_object import Segmentation
from tqdm import tqdm #Une petite barre de progression on sait jamais ca peut etre long

def main(path_json,path_image,liste_seg,interet = True,**kwargs):

    if 'reshape' in kwargs:
        reshape = kwargs['reshape'] 
    else:
        reshape = (512,512)     

    seg = Segmentation(path_json,path_image,liste_seg,reshape)

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
            seg.save()
        
        else: #Autre cas
            for segmentation in range(len(seg.df_json['regions'][image_id])):
                seg.create_polygon(image_id,segmentation)
            seg.segmentation_image()
            seg.resize_image()
            seg.save()








if __name__ == "__main__":

    path_json = "/home/yfrendo/Data/DATASET MorphoTique/Ixodes_masques/anotation.json"
    path_image = "/home/yfrendo/Data/DATASET MorphoTique/0-Ixodes/"
    liste_seg = ["Bouclier","Abdomen",'Rostre']
    main(path_json,path_image,liste_seg)