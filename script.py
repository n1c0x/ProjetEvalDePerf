#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy.special as sps
from scipy.stats import zipf


def rand_duree() :
	return np.random.random()*240

a=1.2
np.set_printoptions(precision=3)
i = 0

topologie = open("topo.top", "r")
trafic = open("traff.traf", "r")
script = open("script.tcl","w")

script.write("""
#create simulator
set ns [new Simulator]

# protocole de routage DV: distance vector LS: link state
$ns rtproto DV

proc finish {} {
	exit 0
}

""")

lignes_topo  = topologie.readlines()
lignes_trafic  = trafic.readlines()

noeuds_tries_orig = []
noeuds_extr = []
capacite = []
delai = []
nb_noeuds = 26

noeuds_traf_src = []
noeuds_traf_dst = []
liste_total_volume = []
nb_flux = 0

for ligne in lignes_topo:
	contenu = np.array(ligne.split())
	noeuds_tries_orig.append(contenu[0])
	noeuds_extr.append(contenu[1])
	capacite.append(contenu[2])
	delai.append(contenu[3])

for ligne in lignes_trafic:
	contenu = np.array(ligne.split())
	noeuds_traf_src.append(contenu[0])
	noeuds_traf_dst.append(contenu[1])
	liste_total_volume.append(contenu[2])
	nb_flux += 1
	
# Création des liens
noeuds_tries_orig_uniques = list(set(noeuds_tries_orig))
noeuds_tries_orig_uniques.sort(key=int)

# Transformation de string vers int
noeuds_tries_orig_uniques = [int(i) for i in noeuds_tries_orig_uniques]


while i < nb_noeuds:
	script.write('set n(')
	script.write(str(i))
	script.write(""") [$ns node]
""")
		
	i += 1

noeuds_tries_orig = [int(i) for i in noeuds_tries_orig]
nb_liens = len(noeuds_tries_orig)

script.write('\n\n')

i = 0
while i < nb_liens:
	script.write('$ns duplex-link $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') '+str(capacite[i])+'Mb '+str(delai[i])+'ms DRR\n')
	script.write('set file'+str(noeuds_tries_orig[i])+str(noeuds_extr[i])+' [open traces/'+str(noeuds_tries_orig[i])+'-'+str(noeuds_extr[i])+'.tr w]\n')
	script.write('$ns trace-queue $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') $file'+str(noeuds_tries_orig[i])+str(noeuds_extr[i])+'\n')
	script.write('$ns queue-limit $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') 10\n\n')
	i += 1

script.write("\n")

compteur_flux = 0
somme_volume = 0
while compteur_flux < nb_flux:
	segmentSize = 0
	compteur_volume = 0
	for compteur_volume in liste_total_volume:
		compteur_volume = compteur_volume.astype(int)
		iterateur_sous_flux = 0
		while somme_volume < compteur_volume*1024*8 :
			taille_segment_tcp = np.random.zipf(a, 1)

			segmentSize = np.int(taille_segment_tcp[0])

			script.write('set null('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') [new Agent/TCPSink/Sack1/DelAck]\n')
			script.write('$ns attach-agent $n('+str(noeuds_traf_src[compteur_flux])+') $null('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+')\n')
			script.write('set tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') [new Agent/TCP]\n')
			script.write('$ns attach-agent $n('+str(noeuds_traf_dst[compteur_flux])+') $tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+')\n')
			script.write('$ns connect $tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') $null('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+')\n')
			script.write('$tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') set packetSize_ 1500\n')

			script.write('set ftp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') [new Application/FTP]\n')
			script.write('$ftp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') set type_ FTP\n')
			script.write('$ftp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') attach-agent $tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+')\n')
			script.write('$ns at '+str(rand_duree())+' "$ftp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') send '+str(segmentSize)+'"\n\n')

			somme_volume = somme_volume + taille_segment_tcp[0]
			somme_volume = np.uint64(somme_volume)
			iterateur_sous_flux += 1
	somme_volume = 0
	compteur_flux += 1

script.write('$ns at 300.0 "finish"\n\n')
script.write('# Run simulation\n')
script.write('$ns run')

topologie.close()
trafic.close()
script.close()

