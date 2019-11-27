-- A SAVOIR 
        /*  1. Avec postgres il est possible de se connecter aux bases de données autres : 
            (Oracle, ESRI, Microsoft SQLServer, Spatialite)
            
            2. Les différents outils qui peuvent communiquer avec SQL pour d'autres utilité :
               ogr2ogr pour transformer les fichiers spatiale (kml, shp, ...) en table SQL
               raster2pgsql pour mettre en forme les fichier raster
               FME automatisation d'execution
               QGIS pour gestion SIG (ogr le fait très bien aussi)            
        */

-- CONNEXION A SQL A PARTIR DE LA CMD
/*  cd Program Files <x86>\PostgresSQL\10\bin  */
psql -U postgres -d postgres -- pour se co sur la data de base  -- mettre le mot de passe    
CREATE DATABASE master;
        -- ctrl + C pour sortir de la base de donnée postgres de base 
psql -U postgres -d master -h 127.0.0.1 -p 5432 -- -h pour serveur -p pour port
CREATE EXTENSION postgis;

-- CREATION DATABASE AVEC EXTENSION POSTGIS 
CREATE DATABASE master;
CREATE EXTENSION postgis;

-- LANCER UN FICHIER 
psql.exe -U postgres -d master -f D:\Axel\Documents\Brain\MASTER_GeoNum\M2\PostGIS\formation.sql

-- ENCODAGE : 
SET client_encoding = latin1; 
-- REV 1 selectionner toutes les données de la table parcelle
SELECT * FROM parcelle;

-- REV 2  compter toutes les données de la table parcelle
SELECT count(*) FROM parcelle;

-- REV 3 afficher toutes les types d'équipements de la table equipement
SELECT distinct theme FROM equipement;

SELECT theme FROM equipement
GROUP BY theme;

SELECT theme, count(*) FROM equipement
GROUP BY theme; 

-- REV 4 selectionner seulement les équipements culturels
SELECT theme FROM equipement
WHERE theme = 'Equipement culturel';

SELECT theme FROM equipement
WHERE theme LIKE 'cul%' ; 

-- REV 5 faire une jointure entre la table parcelle et commune pour recup les parcelle de la commune Caen
SELECT * FROM parcelle
LEFT JOIN commune ON commune.nom = parcelle.commune
AND commune.nom = 'CAEN';

SELECT * FROM parcelle
LEFT JOIN commune ON ST_Within(commune.geom,parcelle.geom)
AND commune.nom = 'CAEN';

-- REV 6 compter toutes les parcelles  
SELECT commune.nom, count(*) as NB_parcelle FROM parcelle
LEFT JOIN commune ON ST_Within(commune.geom,parcelle.geom)
GROUP BY commune.nom
HAVING count(*) > 2500;

-- REV 7 lister tout les équipement par theme avec une limit de 5
SELECT * FROM equipement

LIMIT 5

