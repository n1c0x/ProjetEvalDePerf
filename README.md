# Documentation

## Utilisation des scripts
#### Génération du script TCL
Le script généré est nommé ```script.tcl```
```
#> ./script.py
```

#### Lancement de la simulation
```
#> ns script.tcl
```

##Informations supplémentaires
Les traces sont générées dans un dossier ```traces``` situé dans le dossier courant. Un fichier par lien est ainsi crée. 

Le fichier plot.py sert à générer des statistiques simples à partir des fichiers de trace. Aucun autre fichier ne doit se trouver dans le dossier contenant les fichiers de trace lorsque ```plot.py``` est lancé. En plus des statistiques, un graphe en camembert par fichier représentant le pourcentage de paquets perdus, reçus, ajoutés et enlevés de la file d'attente est généré.

Les fichiers présents dans l'archive ```traces.tar.gz``` sont les fichiers de trace après plusieurs simulations. Dans le dossier ```traces_pertes```, on trouve les traces générées lorsque que le réseau a été configuré afin de générer des pertes. Les fichiers trace du dossier ```traces_sans_pertes``` ne comportent que très peu de pertes.