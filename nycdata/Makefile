all: download_data process_addresses process_buildings process_boundary \
	process_councildistricts process_parcels process_zipcodes

clean: clean_db clean_processed clean_raw

prepare_processed:
	mkdir -p processed
	mkdir -p processed/parcels

clean_processed:
	rm -rf processed/parcels

clean_raw:
	rm -rf raw/MapPLUTO

clean_db:
	-psql -q -c "DROP TABLE parcels" -d llnyc

clean_data:
	rm -rf raw

download_data:
	mkdir -p raw
	download_pluto

download_pluto:
	mkdir -p raw/MapPLUTO
	curl -L "http://www.nyc.gov/html/dcp/download/bytes/bx_mappluto_14v1.zip" -o raw/MapPLUTO/Bronx.zip
	unzip raw/MapPLUTO/Bronx.zip -d raw/MapPLUTO/Bronx
	curl -L "http://www.nyc.gov/html/dcp/download/bytes/bk_mappluto_14v1.zip" -o raw/MapPLUTO/Brooklyn.zip
	unzip raw/MapPLUTO/Brooklyn.zip -d raw/MapPLUTO/Brooklyn
	curl -L "http://www.nyc.gov/html/dcp/download/bytes/mn_mappluto_14v1.zip" -o raw/MapPLUTO/Manhattan.zip
	unzip raw/MapPLUTO/Manhattan.zip -d raw/MapPLUTO/Manhattan
	curl -L "http://www.nyc.gov/html/dcp/download/bytes/qn_mappluto_14v1.zip" -o raw/MapPLUTO/Queens.zip
	unzip raw/MapPLUTO/Queens.zip -d raw/MapPLUTO/Queens
	curl -L "http://www.nyc.gov/html/dcp/download/bytes/si_mappluto_14v1.zip" -o raw/MapPLUTO/Staten_Island.zip
	unzip raw/MapPLUTO/Staten_Island.zip -d raw/MapPLUTO/Staten_Island

process_parcels: prepare_processed
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite processed/parcels/Bronx.shp raw/MapPLUTO/Bronx/Bronx/BXMapPLUTO.shp
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite processed/parcels/Brooklyn.shp raw/MapPLUTO/Brooklyn/Brooklyn/BKMapPLUTO.shp
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite processed/parcels/Manhattan.shp raw/MapPLUTO/Manhattan/Manhattan/MNMapPLUTO.shp
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite processed/parcels/Queens.shp raw/MapPLUTO/Queens/Queens/QNMapPLUTO.shp
	ogr2ogr -simplify 0.2 -t_srs EPSG:4326 -overwrite processed/parcels/Staten_Island.shp raw/MapPLUTO/Staten_Island/Staten_Island/SIMapPLUTO.shp

import_parcels:
	shp2pgsql -D -c -I processed/parcels/parcels.shp parcels | psql -d nola
