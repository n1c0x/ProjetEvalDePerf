#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os

dossier_dest = 'traces'
dossier_dest_graphe = 'graphes'
liste_fichiers = os.listdir(dossier_dest)

noeud_max_pertes = []
res = open("result.res","w")

for filename in liste_fichiers :

	trace = open(dossier_dest+'/'+filename, 'r')
	lignes_traces = trace.readlines()
	trace.close()

	contenu = []

	id_trace = 0
	action = []
	temps = []
	noeud_src = []
	noeud_dst = []
	type_paquet = []
	taille_paquet = []
	flags = []
	id_flux = []
	addr_noeud_src = []
	addr_noeud_dst = []
	seq = []
	id_paquet = []

	nb_paquets = 0
	nb_paquets_perdus = []
	nb_paquets_recus = []
	nb_paquets_ajoutes = []
	nb_paquets_enleves = []

	for ligne in lignes_traces :
		contenu = np.array(ligne.split())
		if contenu[0] == 'd':
			nb_paquets_perdus.append(contenu[1])
		if contenu[0] == 'r':
			nb_paquets_recus.append(contenu[1])
		if contenu[0] == '+':
			nb_paquets_ajoutes.append(contenu[1])
		if contenu[0] == '-':
			nb_paquets_enleves.append(contenu[1])
		nb_paquets += 1

	src = filename.split('-')[0]
	dst = filename.split('-')[1]
	
	res.write('Du noeud '+src+' vers '+dst+'\n')
	res.write(str(nb_paquets)+' Paquets traités\n')
	res.write('----------------------------\n')
	res.write('\tNombre de paquets perdus: '+str(len(nb_paquets_perdus))+'\n')
	res.write('\tNombre de paquets reçus: '+str(len(nb_paquets_recus))+'\n')
	res.write('\tNombre de paquets ajoutés: '+str(len(nb_paquets_ajoutes))+'\n')
	res.write('\tNombre de paquets enlevés: '+str(len(nb_paquets_enleves))+'\n')
	res.write('\n')

	pourcent_pertes = (len(nb_paquets_perdus)/nb_paquets)*100
	noeud_max_pertes.append(pourcent_pertes)

	pourcent_recus = (len(nb_paquets_recus)/nb_paquets)*100
	pourcent_ajoutes = (len(nb_paquets_ajoutes)/nb_paquets)*100
	pourcent_enleves = (len(nb_paquets_enleves)/nb_paquets)*100
	
	plt.figure()
	
	labels = [r'Paquets perdus '+str(pourcent_pertes.__round__(2))+'%',r'Paquets reçus '+str(pourcent_recus.__round__(2))+'%',r'Paquets ajoutés '+str(pourcent_ajoutes.__round__(2))+'%',r'Paquets enlevés '+str(pourcent_enleves.__round__(2))+'%']
	sizes = [pourcent_pertes,pourcent_recus,pourcent_ajoutes,pourcent_enleves]
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
	
	patches, texts = plt.pie(sizes, colors=colors, startangle=90)
	plt.legend(patches, labels, loc="best")
	plt.axis('equal')

	plt.savefig(dossier_dest_graphe+'/'+filename+'.png')
	plt.close()