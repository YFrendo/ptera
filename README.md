# PTERA
## PréTraitEment Rapide des fichiers viA

Petit script qui permet de renvoyer des images (JPEG) à partir des JSON des ségmentations fournis par VIA  
Variables d'entrées:  
* Chemin d'accès vers le fichier JSON des segmentations
* Chemin d'accès vers le fichier contenant les images segmentés
* Largeur des images désiré (optionel par défault 512px)
* Hauteur des images désiré (optionel par défault 512px)  
  
Ce script permet de créer des images JPEG représentant les segmentations mais également de croper les images sur les zones d'intéret désigné par la personne aillant
fait la segmentation. Il permet également de redimenssioner les images et les masques aux dimensions voulu.

Le script va créer 2 dossier Images et Masques à l'endroit de l'exécution et va ranger dedans les images et masques optenues.  

## Instruction pour VIA  

Les instructions pour installer et utiliser VIA sont ici : [via](https://www.robots.ox.ac.uk/~vgg/software/via/)  
**Attention les majuscules sont importantes!**  
Pour notre segmentation nous avons besoin de 2 Attributes :
* 'Region' qui est une checkbox avec 3 id:
  * 'Rostre'
  * 'Bouclier'
  * 'Abdomen'
* 'Tique' qui est une checkbox avec 2 id:
  * 'oui'
  * 'non' (cocher la case par défault)
  
