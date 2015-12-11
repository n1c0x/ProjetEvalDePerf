# Utilisation des scripts


## Génération du script TCL
Le script généré est nommé ```script.tcl```
```
#> ./script.py
```

## Utilisation de ns
```
#> ns script.tcl
```

Les traces sont générées dans un dossier ```traces``` situé dans le dossier courant. Un fichier par lien est ainsi crée. 

Le fichier plot.py sert à générer des statistiques simples à partir des fichiers de trace. Aucun autre fichier ne doit se trouver dans le dossier contenant les fichiers de trace. En plus des statistiques, un graphe en camembert représentant le pourcentage de paquets perdus, reçus, ajoutés et enlevés de la file d'attente