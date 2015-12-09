#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy.special as sps
from scipy.stats import zipf


def rand_duree() :
	return np.random.random()*4

#liste_total_volume = 500000
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

#set f [open my.dat w]
#$ns trace-all $f
#set nf [open out2.nam w]
#$ns namtrace-all $nf

proc finish {} {
	#global ns trace_all
	#$ns flush-trace
	#Close the NAM trace file
	#close $trace_all
	#Execute NAM on the trace file
	#exec nam -a out2.nam &
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

# initialisation de la taille du tableau
# nb_liens = len(noeuds_tries_orig_uniques)

while i < nb_noeuds:
	script.write('set n(')
	#script.write(str(noeuds_tries_orig_uniques[i]))
	script.write(str(i))
	script.write(""") [$ns node]
""")
		
	i += 1

#nb_liens = 0
noeuds_tries_orig = [int(i) for i in noeuds_tries_orig]
nb_liens = len(noeuds_tries_orig)

# Ligne blanche
script.write('\n\n')

i = 0
while i < nb_liens:
	script.write('$ns duplex-link $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') '+str(capacite[i])+'Mb '+str(delai[i])+'ms DropTail\n')
	script.write('set file'+str(noeuds_tries_orig[i])+str(noeuds_extr[i])+' [open traces/queue'+str(noeuds_tries_orig[i])+str(noeuds_extr[i])+'.tr w]\n')
	script.write('$ns trace-queue $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') $file'+str(noeuds_tries_orig[i])+str(noeuds_extr[i])+'\n')
	script.write('$ns queue-limit $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') 10\n\n')
	i += 1

# Création des couples
'''
noeuds_traf_src
noeuds_traf_dst
liste_total_volume
nb_flux
'''

# Ligne blanche
script.write("\n")

i = 0
while i < nb_flux:
	# script.write('set null('+str(noeuds_traf_src[i])+'_'+str(noeuds_traf_dst[i])+') [new Agent/Null]\n')
	# script.write('$ns attach-agent $n('+str(noeuds_traf_src[i])+') $null('+str(noeuds_traf_src[i])+'_'+str(noeuds_traf_dst[i])+')\n')
	# script.write('set tcp('+str(noeuds_traf_src[i])+'_'+str(noeuds_traf_dst[i])+') [new Agent/UDP]\n')
	# script.write('$ns attach-agent $n('+str(noeuds_traf_dst[i])+') $tcp('+str(noeuds_traf_src[i])+'_'+str(noeuds_traf_dst[i])+')\n')
	# script.write('$ns connect $tcp('+str(noeuds_traf_src[i])+'_'+str(noeuds_traf_dst[i])+') $null('+str(noeuds_traf_src[i])+'_'+str(noeuds_traf_dst[i])+')\n')
	# script.write('$tcp('+str(noeuds_traf_src[i])+'_'+str(noeuds_traf_dst[i])+') set packetSize_ 1500\n\n')
	# Envoi de données à un temps donné ns. En octets. at 0 "$tcp send 1000"
	i += 1

compteur_flux = 0
somme_volume = 0
while compteur_flux < nb_flux:
	segmentSize = 0
	compteur_volume = 0
	for compteur_volume in liste_total_volume:
		compteur_volume = compteur_volume.astype(int)*1000000*8
		#compteur_volume = compteur_volume.astype(int)
		iterateur_sous_flux = 0
		while somme_volume < compteur_volume :
			taille_segment_tcp = np.random.zipf(a, 1)
			segmentSize = taille_segment_tcp[0]

			script.write('set null('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') [new Agent/TCPSink]\n')
			script.write('$ns attach-agent $n('+str(noeuds_traf_src[compteur_flux])+') $null('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+')\n')
			script.write('set tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') [new Agent/TCP]\n')
			script.write('$ns attach-agent $n('+str(noeuds_traf_dst[compteur_flux])+') $tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+')\n')
			script.write('$ns connect $tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') $null('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+')\n')
			script.write('$tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') set packetSize_ 1500\n')

			script.write('set ftp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') [new Application/FTP]\n')
			script.write('$ftp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') attach-agent $tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+')\n')
			script.write('$ns at '+str(rand_duree())+' "$ftp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') start"\n')
			#script.write('$ns at '+str(rand_duree())+' "$tcp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') send size '+str(segmentSize)+'"\n')
			script.write('$ns at '+str(4.5)+' "$ftp('+str(noeuds_traf_src[compteur_flux])+'_'+str(noeuds_traf_dst[compteur_flux])+'_'+str(iterateur_sous_flux)+') stop"\n\n')
			somme_volume = somme_volume + taille_segment_tcp[0]
			iterateur_sous_flux += 1
	somme_volume = 0
	compteur_flux += 1

# while i > 0:
# 	script.write('$ns at '+str(4.5)+' "$udp('+str(i-1)+') stop"\n')
# 	i -= 1

script.write('$ns at 5.0 "finish"\n\n')
script.write('# Run simulation\n')
script.write('$ns run')

'''
i = 0
for i in liste_total_volume:
	i = i.astype(int)
	while somme_volume < i :
		# s est un tableau
		s = np.random.zipf(a, 1)
		#print(s)
		somme_volume = somme_volume + s[0]
		#i = i+1
	#print("{} : {}\n\n\n".format("somme_volume", somme_volume))


somme_volume = 0
for j in liste_total_volume:
	j = j.astype(int)
	while somme_volume < j :
		# s est un tableau
		s = np.random.zipf(1.2, 1)
		print(s)
		somme_volume = somme_volume + s[0]
'''



#print("{}: {}".format("Nombre de flux",nb_flux))
#print("{}: {} {}".format("liste_total_volume", liste_total_volume, "Go"))
#print("{}: {}".format("somme_volume", somme_volume))


topologie.close()
trafic.close()
script.close()

