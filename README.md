# APP

Le projet APP est en lien avec l'utilisation du modèle d'apprentissage profond GeoDeepLearning de Ressources naturelles Canada (https://github.com/NRCan/geo-deep-learning). 
Il a comme but d'évaluer les indices topographiques produits à partir de modèles numériques de terrain dans un contexte d'apprentissage profond. 
Les statistiques produites lors de l'entraînement des modèles serviront à comparer les différents apports des indices pour identifier lhydrologie de surface. 
Les scripts produits pour ce projet peuvent être subdivisés en deux groupes :
- La production d'indices topographiques à partir de modèles numériques de terrain. Ces indices permettent d'évaluer la propension d'un pixel à contenir de l'eau.
- L'analyse des statistiques produites lors de l'entraînement du modèle d'apprentissage profond GeoDeepLearning. 


***Indices topographiques***
Le script script_IT.py permet la production de l'indice Topographic Wetness Index (TWI) de Beven & Kirkby (1979) à l'aide de l'algorithme d'écoulement D8 (O'Callaghan & Mark, 1984), Dinf (Quinn et al., 1995), FD8 (Freeman, 1991). Le script peut être appelé en ligne de commmande de la manière suivante: 
nomduscript.py -d path/to/input/directory/ -o path/to/output/directory/ -t type d'indice voulu

Il est aussi possible de choisir l'option -h pour avoir accès à l'aide.

L'indice de Hjerdt (Hjerdt et al., 2004) peut être produit avec le script Hjerdt.py. Le script n'est présentement pas disponible en ligne de commande, mais il le sera sous peut. 

Des fichiers tif des modèles numériques de terrain sont disponibles gratuitement sur : https://ouvert.canada.ca/data/fr/dataset/768570f8-5761-498a-bd6a-315eb6cc023d


***Analyse des statistiques calculées lors des entraînements***

Le script plot_GDL_stats.py permet de ressortir et de représenter divers statistiques issues de l'entraînement de GeoDeepLearning.
Trois types de graphiques sont possibles : 
1. Le taux de perte (loss) selon le taux d’apprentissage (learning rate). Ce graphique requiert les résultats de plusieurs entraînements ainsi que la valeur du taux d’apprentissage utilisé dans le nom du dossier. 
2. L’évolution d’une statistique selon les époques. Cette statistique est calculée lors de la validation d’un entraînement, pour chaque classe présente dans la classification utilisée; 
3. Une comparaison entre les taux de perte de l’entraînement et de la validation selon les époques. 

Le script est appelé avec la ligne de commande :
python plot_GDL_stats.py [plots] [inFolders] {-st, --stat} {-x, --xextent} {-y, --yextent} {-s, --save} {-r, --replace}
où
[..] : indique les arguments obligatoires;
{..} : indique les arguments optionnels;
plots : type de graphique voulu parmis loss_vs_learning_rate, val_stat_vs_epoch et trn_vs_val_loss;
inFolders : dossier(s) contenant le ou les résultats d'entraînements nécessaires pour le graphique. Seulement le graphique 'loss_vs_learning_rate' requiert plus d'un dossier;
stat : statistique de validation à représenter lorsque le graphique est de type 'val_stat_vs_epoch'. Choisir parmi val_fscore, val_loss, val_precision et val_recall;
xextent : valeurs minimale et maximale de l'axe des x. Incrire les deux valeurs dans l'ordre ascendant, séparées par un espace;
yextent : valeurs minimale et maximale de l'axe des y. Incrire les deux valeurs dans l'ordre ascendant, séparées par un espace;
save : emplacement et nom du fichier où le graphique sera enregistré;
replace : à écrire pour pouvoir remplacer un fichier qui existe déjà.

Librairies requises : argparse, matplotlib, os.path, pandas

Contraintes présentes :
- Un seul graphique peut être produit à la fois.
- Les logs contenant les statistiques sont directement dans le ou les dossiers spécifié par l'utilisateur, pas dans des sous-dossiers.
- Les noms des dossiers doivent contenir la valeur utilisée pour le taux d'apprentissage lors de l'entraînement.

Les résultats de trois entraînements de GeoDeepLearning sont disponibles dans le dossier Resultats_GDL du projet APP.
