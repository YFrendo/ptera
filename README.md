# PTERA
## PréTraitEment Rapide des fichiers viA

Petit script qui permet de renvoyer des images (JPEG) à partir des JSON des ségmentations fournis par VIA  

Variables d'entrées:  
* Chemin d'accès vers le fichier JSON des segmentations
* Chemin d'accès vers le fichier contenant les images segmentés
* Nom des segmentations séparé par une virgule (senssible à la case)
* Largeur + Hauteur des images désiré (optionel -s par défault 512.512px)
* Valeur de l'augmentation compris entre 0 et 9 (optionel - A par défault 0)
* Chemin d'accès vers le dossier de l'enregistrement (optionel -E par défault '.')
* Activation de la découpe de la zone d'intéret (optionel -c par défault True)  
  
Ce script permet de créer des images JPEG représentant les segmentations mais également de croper les images sur les zones d'intéret désigné par la personne aillant fait la segmentation. Il permet également de redimenssioner les images et les masques aux dimensions voulu.
Une augmentation est possible avec l'application alléatoire d'une transformation (voir détails à la section augmentation)

Le script va créer 2 dossier Images et Masques à l'endroit désigné et va ranger dedans les images et masques optenues.  

## Instruction pour VIA  

Les instructions pour installer et utiliser VIA sont ici : [via](https://www.robots.ox.ac.uk/~vgg/software/via/)  
**Attention les majuscules sont importantes!** *Sera corrigé plus tard*
Pour notre segmentation nous avons besoin de 2 Attributes :
* 'Segmentation' qui est une checkbox avec maximum 5 id
* 'Interet' qui est une checkbox avec 2 id:
  * 'oui'
  * 'non' (cocher la case par défault)  

### Configuration des attributes 

![Image pour l'attribute Segmentation](https://github.com/YFrendo/ptera/blob/main/images_readme/Segmentation.png?raw=true)
![Image pour l'attribute Interet](https://github.com/YFrendo/ptera/blob/main/images_readme/Interet.png?raw=true)  

### Segmentation et annotation  

![Segmentation](https://github.com/YFrendo/ptera/blob/main/images_readme/Image_segmente.png?raw=true)
![Annotations](https://github.com/YFrendo/ptera/blob/main/images_readme/Annotations.png?raw=true)  

## Utilisation de PTERA  

Il suffit d'installer les requirements disponible dans le git et de lancer la commande suivante à l'endroit où vous voulez que les fichiers soit créer:  
`python3 main.py [path du fichier JSON des annotations] [path du dossier contenant les images] [Nom des segmentations séparé par une virgule ]-s [Largeur,Hauteur] -A [Valeur de l'augmentation] -E [path enregistrement] -c [Crop]`

### Résultats de PTERA

![Image pour l'attribute Region](https://github.com/YFrendo/ptera/blob/main/images_readme/Resultat_ptera.png?raw=true)

### Augmentation

Une augmentation est possible jusque à 9 fois

## Améliorations possibles

Quelques point d'améliorations possibles et idées pour le futur:
* Gestion des cas où il y a plusieurs tiques 
