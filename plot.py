#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os

files = {}

#for filename in os.listdir(os.getcwd()+'/traces_small/') :
#	files[filename] = filename
#	trace = open('traces_small/'+filename, "r")
#	files["trace" + str(filename)] = trace.readlines()

	#print(files['queue017.tr'])


#for filename in files : 
trace = open('traces_small/queue017.tr', "r")
lignes_traces = trace.readlines()

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

nb_paquets_perdus = []

for ligne in lignes_traces :
	contenu = np.array(ligne.split())
	if contenu[0] == 'd':
		nb_paquets_perdus.append(contenu[1])
		#print("Paquet perdu à "+contenu[1])



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


print("Nombre de paquets perdus: "+str(nb_paquets_perdus))

# definition de l'échelle (log ou pas)
# plt.yscale('log')

plt.plot(temps, nb_paquets_perdus)
plt.ylabel('Test')
plt.xlabel('Temps')
plt.show()