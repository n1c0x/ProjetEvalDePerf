# mettre TCP en flux (et pas UDP)
# tcp send size
# $tcp(0) set packetSize_ 1500
# tcp send size (taille du flux tcp -> zipf)
# nom du flux: 0_1_1
# 0: source
# 1: destination
# 1: no du fragment de flux

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sps
from scipy.stats import zipf

def rand_duree() :
	return np.random.random()*4

#volume = 500000
a=1.2
np.set_printoptions(precision=3)
somme = 0
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
	#global ns nf
	#$ns flush-trace
	#Close the NAM trace file
	#close $nf
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
nb_liens = 26

noeuds_traf_src = []
noeuds_traf_dst = []
volume = []
taille_traf = 0

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
	volume.append(contenu[2])
	taille_traf += 1
	


# Création des liens

noeuds_tries_orig_uniques = list(set(noeuds_tries_orig))
noeuds_tries_orig_uniques.sort(key=int)

# Transformation de string vers int
noeuds_tries_orig_uniques = [int(i) for i in noeuds_tries_orig_uniques]

# initialisation de la taille du tableau
taille = len(noeuds_tries_orig_uniques)

while i < nb_liens:
	script.write('set n(')
	#script.write(str(noeuds_tries_orig_uniques[i]))
	script.write(str(i))
	script.write(""") [$ns node]
""")
		
	i += 1

#taille = 0
noeuds_tries_orig = [int(i) for i in noeuds_tries_orig]
taille = len(noeuds_tries_orig)

# Ligne blanche
script.write('\n\n')

i = 0
while i < taille:
	script.write('$ns duplex-link $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') '+str(capacite[i])+'Mb '+str(delai[i])+'ms DropTail\n')
	script.write('set file'+str(noeuds_tries_orig[i])+str(noeuds_extr[i])+' [open traces/queue'+str(noeuds_tries_orig[i])+str(noeuds_extr[i])+'.tr w]\n')
	script.write('$ns trace-queue $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') $file'+str(noeuds_tries_orig[i])+str(noeuds_extr[i])+'\n')
	script.write('$ns queue-limit $n('+str(noeuds_tries_orig[i])+') $n('+str(noeuds_extr[i])+') 10\n\n')
	i += 1

# Création des couples
'''
noeuds_traf_src
noeuds_traf_dst
volume
taille_traf
'''

# Ligne blanche
script.write("\n")

i = 0
while i < taille_traf:
	script.write('set null('+str(i)+') [new Agent/Null]\n')
	script.write('$ns attach-agent $n('+str(noeuds_traf_src[i])+') $null('+str(i)+')\n')
	script.write('set udp('+str(i)+') [new Agent/UDP]\n')
	script.write('$ns attach-agent $n('+str(noeuds_traf_dst[i])+') $udp('+str(i)+')\n')
	script.write('$ns connect $udp('+str(i)+') $null('+str(i)+')\n\n')
	# Envoi de données à un temps donné ns. En octets. at 0 "$tcp send 1000"
	i += 1

i = 0
while i < taille_traf:
	packetSize = 0
	for j in volume:
		j = j.astype(int)
		while somme < j :
			s = np.random.zipf(a, 1)
			packetSize = s[0]
			script.write('$udp('+str(i)+') set packetSize_ '+str(packetSize)+'\n')
			script.write('$ns at '+str(rand_duree())+' "$udp('+str(i)+') start"\n\n')
			somme = somme + s[0]
	somme = 0
	i += 1

while i > 0:
	script.write('$ns at '+str(4.5)+' "$udp('+str(i-1)+') stop"\n')
	i -= 1

script.write('$ns at 5.0 "finish"\n\n')
script.write('# Run simulation\n')
script.write('$ns run\n')

'''
i = 0
for i in volume:
	i = i.astype(int)
	while somme < i :
		# s est un tableau
		s = np.random.zipf(a, 1)
		#print(s)
		somme = somme + s[0]
		#i = i+1
	#print("{} : {}\n\n\n".format("Somme", somme))


somme = 0
for j in volume:
	j = j.astype(int)
	while somme < j :
		# s est un tableau
		s = np.random.zipf(1.2, 1)
		print(s)
		somme = somme + s[0]
'''



#print("{}: {}".format("Nombre de flux",taille_traf))
#print("{}: {} {}".format("Volume", volume, "Go"))
#print("{}: {}".format("Somme", somme))


topologie.close()
trafic.close()
script.close()

