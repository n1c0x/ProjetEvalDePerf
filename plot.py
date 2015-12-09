#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os

dossier_dest = 'traces_Mb'
liste_fichiers = os.listdir(dossier_dest)

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

		'''
		action.append(contenu[0])
		temps.append(contenu[1])
		noeud_src.append(contenu[2])
		noeud_dst.append(contenu[3])
		type_paquet.append(contenu[4])
		taille_paquet.append(contenu[5])
		flags.append(contenu[6])
		id_flux.append(contenu[7])
		addr_noeud_src.append(contenu[8])
		addr_noeud_dst.append(contenu[9])
		seq.append(contenu[10])
		id_paquet.append(contenu[11])
		'''

	src = filename.split('-')[0]
	dst = filename.split('-')[1]
	#print(filename.split('-'))
	print('Du noeud '+src+' vers '+dst)
	print(str(nb_paquets)+' Paquets traités')
	print('----------------------------')
	print('\tNombre de paquets perdus: '+str(len(nb_paquets_perdus)))
	print('\tNombre de paquets reçus: '+str(len(nb_paquets_recus)))
	print('\tNombre de paquets ajoutés: '+str(len(nb_paquets_ajoutes)))
	print('\tNombre de paquets enlevés: '+str(len(nb_paquets_enleves)))
	print('\n')

	pourcent_pertes = (len(nb_paquets_perdus)/nb_paquets)*100
	pourcent_recus = (len(nb_paquets_recus)/nb_paquets)*100
	pourcent_ajoutes = (len(nb_paquets_ajoutes)/nb_paquets)*100
	pourcent_enleves = (len(nb_paquets_enleves)/nb_paquets)*100
	#print(str(pourcent_pertes.__round__(2))+'%  paquets perdus')

	
	#plt.plot(temps, seq)
	#plt.ylabel('Test')
	#plt.xlabel('Temps')
	plt.figure()
	
	labels = [r'Paquets perdus '+str(pourcent_pertes.__round__(2))+'%',r'Paquets reçus '+str(pourcent_recus.__round__(2))+'%',r'Paquets ajoutés '+str(pourcent_ajoutes.__round__(2))+'%',r'Paquets enlevés '+str(pourcent_enleves.__round__(2))+'%']
	#values = [pourcent_pertes,pourcent_recus,pourcent_ajoutes,pourcent_enleves]
	sizes = [pourcent_pertes,pourcent_recus,pourcent_ajoutes,pourcent_enleves]
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

	#plt.pie(values, labels=labels, autopct='%.2f')

	patches, texts = plt.pie(sizes, colors=colors, startangle=90)
	plt.legend(patches, labels, loc="best")
	plt.axis('equal')

	plt.savefig(dossier_dest+'/images'+filename+'.png')
	plt.close()
	#plt.show()