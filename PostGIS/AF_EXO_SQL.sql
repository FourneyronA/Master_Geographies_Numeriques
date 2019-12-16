-- A SAVOIR 
        /*  
            1. Avec postgres il est possible de se connecter aux bases de données autres : 
               (Oracle, ESRI, Microsoft SQLServer, Spatialite)
            
            2. Les différents outils qui peuvent communiquer avec SQL pour d'autres utilité :
               ogr2ogr pour transformer les fichiers spatiale (kml, shp, ...) en table SQL
               raster2pgsql pour mettre en forme les fichier raster
               FME automatisation d'execution
               QGIS pour gestion SIG (ogr le fait très bien aussi)  

            3. Favoriser les INNER JOIN plutôt que les WHERE pour les jointures spatiales 
                Car il y a souvent des problèmes d'overpass en multipliant les conditions

            4. Les opérations de POSTGIS sont parfois couteuse en temps de calcule il faut savoir ce qu'on attend :
                        Exemple N°1 ST_Distance (calcule distance) avec ST_Dwithin (object situé dans un objet à XX de distance)
                Pour facilité ses temps de calcule il faut ABSOLUMENT indexer les champs de géométry 
                        Exemple N°2 découpage des lignes permet de limiter les BBOX en fesant plusieurs petites boites plutôt qu'une grosse

            5.  \timing permet d'avoir le temps de calcule 
        */

-- CONNEXION A SQL A PARTIR DE LA CMD
/*  cd Program Files <x86>\PostgresSQL\10\bin  */
--psql -U postgres -d postgres
                                 -- pour se co sur la data de base  -- mettre le mot de passe    
CREATE DATABASE master;
        -- ctrl + C pour sortir de la base de donnée postgres de base 
--psql -U postgres -d master -h 127.0.0.1 -p 5432
                                                 -- -h pour serveur -p pour port
CREATE EXTENSION postgis;

-- CREATION DATABASE AVEC EXTENSION POSTGIS 
CREATE DATABASE master;
CREATE EXTENSION postgis;

-- LANCER UN FICHIER 
-- psql.exe -U postgres -d master -f C:\Users\fourn\Documents\Brain\M2\PostGIS\formation.sql

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


-- Nous indique combien de batiment sont invalide
SELECT count(gid) FROM batiment
WHERE NOT ST_IsValid(geom);


-- Nous indique l'ID des batiments invalide
SELECT gid FROM batiment
WHERE NOT ST_IsValid(geom);

-- transtypage (utilisation seulement en affichage mais possibilité de le faire une un UPDATE)
-- transtypage pour passer d'une chaine de caractère en date 
SELECT '2018-06-01'::date
-- transtypage pour les géométry 
SELECT 'SRID=2154;POINT(0 0)'::geometry
SELECT '01060000206A080000010000000103000000020000000B000000CEB8C418C9781B41'::geometry

-- Creer une chaine de caractère à partir de différent champs
SELECT concat('GEOMINVALID : SRID=',ST_SRID,' avec pour ID : ',gid) FROM batiment
WHERE NOT ST_IsValid(geom);

-- ajouter une colonne geom en 4326
ALTER TABLE parcelle ADD geomWGS84 geometry(Polygon, 4326);

-- 8.1 Créer une géométrie : Essayez de rajouter un objet dans la table batiment 
INSERT INTO batiment (gid, commune, nom, type,created,updated,geom)
VALUES ('580237','14030', 'MonTest',12,'2016-05-02','2016-05-02',
         ST_GeomFromText('MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), ((15 5, 40 10, 10 20, 5 10, 15 5)))', 2154));

-- Montrer les 5 Multipolygone qui contienne le plus de polygone
SELECT gid, ST_NumGeometries(geom)  FROM batiment
ORDER BY ST_NumGeometries(geom) DESC
LIMIT 5;

-- tester si deux ligne font la même distance
SELECT ST_Equals('LINESTRING(0 5,5 1)','LINESTRING(5 1,0 5)');

-- Jointure spatiale via inner join 
SELECT * FROM batiment as b
INNER JOIN equipement as e
ON ST_INTERSECTS(b.geom, e.geom)
WHERE e.theme ilike '%sportif%' ;

-- ST_WITHIN permet de joindre seulement quand une géométry et DANS l'autres
SELECT * FROM batiment as b
INNER JOIN equipement as e
ON ST_Within(b.geom, e.geom);

--Ecrivez une requête qui permet de récupérer les parcelles situées à moins de 200 mètres des equipement dont le nom est “Mairie” 
SELECT p.* FROM parcelle p, equipement e 
WHERE ST_DWithin(p.geom, e.geom,200); --ST_Dwithin > ST_distance si c'est pour savoir si un objet est situé dans une distance
AND e.nom = 'Mairie';

SELECT p.* FROM parcelle p, equipement e WHERE ST_DWithin(p.geom, e.geom,200) AND e.nom = 'Mairie';

/* 
Pour plus tard, gestionnaires de base de données :
Il faut regarder un profilage des tableaux car si petit tableau -> lecture sequentiel plus optimale
ATTENTION si il y a une géométrie -> toujours une index 
possibilité de vérifier la présence de l'index : \d NOM_TABLE
a se moment on a un retour sur les variables indexés
*/

-- Creation d'index
create index idx_parcelle_geom on parcelle using GIST (geom);
create index equipement_geom_idx on equipement using GIST (geom);

-- Pensez a faire des requetes 
