# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 14:15:00 2019

@author: bastien Cahier
"""

def calculDistance(point1,point2):
    #Le calcul de la distance entre deux points est fait en prenant en compte la courbure de la Terre, ce n'est pas une distance sur un plan (x,y)!
    #Ces formules peuvent être trouvées directement en python sur le net
    #les paramètres d'entrée sont au format [lat,lon] --> si format [lon,lat] : penser à inverser les valeurs!
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(point1[0])
    lon1 = radians(point1[1])
    lat2 = radians(point2[0])
    lon2 = radians(point2[1])
    #calcul des deltas Long et Lat
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    #calcul de la distance
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    #distance in Meters
    distance = R * c * 1000 
    return distance


#########################
## calcul distance max ##
#########################
def distanceMax(points,centroide):
	#Fonction pour avoir la distance max entre un nuage de point et un point donné (par exemple le centroide)
	#Fait appel à la fonction de calcul de distance entre deux points
	#Le paramètre "points" est une liste de points de coordonnées de type [[y1,x1],[y2,x2],...,[yn,xn]]

	#Initialisation : la distance Max est la distance entre le premier point de la liste et le centroide
    distMax = calculDistance(centroide,points[0])

    #Boucle qui calcul la distance entre chaque point de la liste et le centroide
    for i in range(len(points)):
        dist = calculDistance(centroide,points[i])
        #Si  distance calculée > distance Max précédente : distance Max devient la distance calculée 
        if dist > distMax :
            distMax = dist
    return distMax


#############################
## calcul distance moyenne ##
#############################
def distanceMoyenne(points,centroide):
    #Fonction pour avoir la distance moyenne entre un nuage de point et un point donné (par exemple le centroide)
    #Fait appel à la fonction de calcul de distance entre deux points
    #Le paramètre "points" est une liste de points de coordonnées de type [[y1,x1],[y2,x2],...,[yn,xn]]

    #initialisation variable qui prendra la somme des distances au fur et à mesure que l'on parcourt la liste des points
    somme_dist = 0 

    #Boucle qui calcule la distance entre chaque point de la liste et le point central
    for i in range(len(points)):
        somme_dist = somme_dist + calculDistance(centroide,points[i])

    #distance moy = somme des distances / nombre de points 
    dist_moy = somme_dist / len(points)
    return dist_moy


