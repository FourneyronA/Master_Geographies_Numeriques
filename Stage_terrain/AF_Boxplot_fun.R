
# . -------------------------------------------------------------------------- =============
# 1 - Chargement des librairies ====
# . -------------------------------------------------------------------------- =============
  
  ### manipulation et traitement de donnees
  library(dplyr) 
  library(tidyr)
  library(tidyverse)
  library(stringr)
  library(readxl) # lectures des fichiers excel plus facilement
  library(readr) # read csv
  
  ### Visualisation carto
  library(sf)
  library(sp)
  library(rgdal)
  library(raster)
# library(mapview)
# library(dbscan)
# library(cartography)

  ### visualisation des donnees 
  library(ggplot2) # la visualisation graph stat
  library(sf)
  library(SpatialPosition)
  library(rayshader)

# . -------------------------------------------------------------------------- =============
# 2 - lecture des données ====
# . -------------------------------------------------------------------------- =============

  setwd (dir ="C:/Users/fourn/Documents/Brain/M2/Stage de terrain/Analyse_profile")
  
  Circular_donnee_H <- st_read(dsn="GCPs_MNS_Circular/GCPs_MNS_Circular.shp", stringsAsFactors = FALSE)
  Double_grid_donnee_C<- st_read(dsn="GCPs_MNS_DoubleGrid_COUPLE/GCPs_MNS.shp", stringsAsFactors = FALSE)
  Grille <- st_read(dsn="GRILLE_GCP/Grille_homogène_10GCP.shp", stringsAsFactors = FALSE)
  Double_grid_donnee_H<- st_read(dsn="GCPs_MNS_DoubleGrid_HOMOGENE/GCPs_MNS_HOMOGENE.shp", stringsAsFactors = FALSE)
  

# . -------------------------------------------------------------------------- =============
# 3 - Remise en forme des données ====
# . -------------------------------------------------------------------------- =============

### CREATION DES DONNEES CIRCULAIRE HOMOGENE 

  Circular_donne_11GCP <- data.frame(Circular_donnee_H$diff_11GCP,"NULL","10","circular","Point homogène")
  names(Circular_donne_11GCP) <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  Circular_donne_20GCP <- data.frame(Circular_donnee_H$diff_20GCP,"NULL","20","circular","Point homogène")
  names(Circular_donne_20GCP)  <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  Circular_donne_30GCP <- data.frame(Circular_donnee_H$diff_30GCP,"NULL","30","circular","Point homogène")
  names(Circular_donne_30GCP)  <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  
  CiculaireH <- rbind(Circular_donne_11GCP, Circular_donne_20GCP, Circular_donne_30GCP)
  rm(Circular_donne_5GCP, Circular_donne_11GCP, Circular_donne_20GCP, Circular_donne_30GCP)
  
  ### CREATION DES DONNEES CIRCULAIRE ALEATOIRE
  
  # Circular_donne_11GCP <- data.frame(Circular_donnee$diff_11GCP,Circular_donnee$distance,"10","circular","Point Aléatoire")
  # names(Circular_donne_11GCP) <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  # Circular_donne_20GCP <- data.frame(Circular_donnee$diff_20GCP,Circular_donnee$distance,"20","circular","Point Aléatoire")
  # names(Circular_donne_20GCP)  <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  # Circular_donne_30GCP <- data.frame(Circular_donnee$diff_30GCP,Circular_donnee$distance,"30","circular","Point Aléatoire")
  # names(Circular_donne_30GCP)  <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  # 
  # CiculaireA <- rbind(Circular_donne_5GCP, Circular_donne_11GCP, Circular_donne_20GCP, Circular_donne_30GCP)
  # rm(Circular_donne_5GCP, Circular_donne_11GCP, Circular_donne_20GCP, Circular_donne_30GCP)
  
  ### CREATION DES DONNEES DOUBLEGRID HOMOGENE 
  
  Double_grid_donne_10GCP <- data.frame(Double_grid_donnee_H$diff_10GCP ,"NULL","10","Double_grid","Point homogène")
  names(Double_grid_donne_10GCP)  <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  Double_grid_donne_30GCP <- data.frame(Double_grid_donnee_H$diff_20GCP,"NULL","20","Double_grid","Point homogène")
  names(Double_grid_donne_30GCP) <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  Double_grid_donne_52GCP <- data.frame(Double_grid_donnee_H$diff_30GCP,"NULL","30","Double_grid","Point homogène")
  names(Double_grid_donne_52GCP) <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  
  Double_gridH <- rbind(Double_grid_donne_10GCP, Double_grid_donne_30GCP, Double_grid_donne_52GCP)
  rm(Double_grid_donne_10GCP, Double_grid_donne_30GCP, Double_grid_donne_52GCP)
  
  ### CREATION DES DONNEES DOUBLEGRID ALEATOIRE 
  
  Double_grid_donne_10GCP <- data.frame(Double_grid_donnee_C$diff_10GCP ,"NULL","10","Double_grid","Point Aléatoire")
  names(Double_grid_donne_10GCP)  <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  Double_grid_donne_30GCP <- data.frame(Double_grid_donnee_C$diff_30GCP,"NULL","30","Double_grid","Point Aléatoire")
  names(Double_grid_donne_30GCP) <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  Double_grid_donne_52GCP <- data.frame(Double_grid_donnee_C$diff_52GCP,"NULL","52","Double_grid","Point Aléatoire")
  names(Double_grid_donne_52GCP) <- c("Marge_Erreur","Distance", "NB_GCP", "prise_de_vue","type_repartition")
  
  Double_gridA <- rbind(Double_grid_donne_10GCP, Double_grid_donne_30GCP, Double_grid_donne_52GCP)
  rm(Double_grid_donne_10GCP, Double_grid_donne_30GCP, Double_grid_donne_52GCP)
  
  ALL_DONNEE <- rbind(CiculaireH, Double_gridA, Double_gridH) # /!\ replacer circulaireA lorsqu'on aura les données
  rm( CiculaireH, Double_gridA, Double_gridH)




# . -------------------------------------------------------------------------- =============
# 4 - Analyses de la qualité des données ====
# . -------------------------------------------------------------------------- =============

# Analyses Boxplot comparaison circulaire / double grid

  graph1 <- ggplot(ALL_DONNEE,aes(x = NB_GCP, y = (Marge_Erreur*100), color = NB_GCP, fill = NB_GCP)) +
    geom_boxplot(alpha = 0.4, color = "grey10", width = 0.40) + 
    geom_jitter(width = 0.25, alpha = 0.4)+
    geom_point(stat ="summary",color = "grey10", fun.y = "mean", size = 5, pch = 3 )+
    labs(x = "Nombre de points GCP utilisés", caption = "Source : Master Géonumérique")+
    ggtitle("Comparaison de la qualité des données pour chaque type de méthode") +
    theme(legend.position="none") +
    scale_y_continuous (name = "Marge d'erreur en centimètre", breaks=c(seq(0,250,25)), limits = c(0,250)) 
    + theme_light()
  
  graph_tot2=graph1+facet_grid(rows=vars(prise_de_vue),
                               cols=vars(type_repartition))
  plot(graph_tot2)
  ggsave(filename = "Tableau_boxplot_comparaison.png")


