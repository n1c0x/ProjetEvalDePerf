#!/bin/awk -f
# '+' -> ajout dans la queue
# '-' -> suppression de la queue
# 'r' -> réception du message
# 'd' -> suppression du message
#
# $1 -> action effectuée
# $2 -> temps
# $3 -> noeud de départ
# $4 -> noeud d'arrivée
# $5 -> type de paquet
# $6 -> taille du paquet
# $7 -> flags
# $8 -> identifiant de flux
# $9 -> adresse du noeud source
# $10 -> adresse du noeud destination
# $11 -> No de séquence
# $12 -> id de paquet unique

BEGIN { }
{	print("Temps\011Taille")
	if($1 == "+"){
		print($2,$11) > FILENAME"+"
	}else if($1 == "-"){
		print($2,$11) > FILENAME"-"
	}else if($1 == "d"){
		print($2,$11) > FILENAME"d"
	}
}
END {  }