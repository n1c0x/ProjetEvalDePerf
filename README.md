# Documentation

Ce programme est dédié à des fin éducatives. Aucune réclamation et aucun support n'est apporté à ce programme.

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
