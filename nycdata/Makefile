all: download_data process_addresses process_buildings process_boundary \
	process_parcels process_zipcodes

clean: clean_db clean_processed clean_raw

prepare_processed:
	mkdir -p processed
	mkdir -p processed/landmarks
	mkdir -p processed/libraries
	mkdir -p processed/nycha
	mkdir -p processed/parcels
	mkdir -p processed/postoffices

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
	curl -L "http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/bx_mappluto_16v1.zip" -o raw/MapPLUTO/Bronx.zip
	unzip raw/MapPLUTO/Bronx.zip -d raw/MapPLUTO/Bronx
	curl -L "http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/bk_mappluto_16v1.zip" -o raw/MapPLUTO/Brooklyn.zip
	unzip raw/MapPLUTO/Brooklyn.zip -d raw/MapPLUTO/Brooklyn
	curl -L "http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/mn_mappluto_16v1.zip" -o raw/MapPLUTO/Manhattan.zip
	unzip raw/MapPLUTO/Manhattan.zip -d raw/MapPLUTO/Manhattan
	curl -L "http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/qn_mappluto_16v1.zip" -o raw/MapPLUTO/Queens.zip
	unzip raw/MapPLUTO/Queens.zip -d raw/MapPLUTO/Queens
	curl -L "http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/si_mappluto_16v1.zip" -o raw/MapPLUTO/Staten_Island.zip
	unzip raw/MapPLUTO/Staten_Island.zip -d raw/MapPLUTO/Staten_Island

process_parcels: prepare_processed
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/parcels/Bronx.shp raw/MapPLUTO/Bronx/BXMapPLUTO.shp
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/parcels/Brooklyn.shp raw/MapPLUTO/Brooklyn/BKMapPLUTO.shp
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/parcels/Manhattan.shp raw/MapPLUTO/Manhattan/MNMapPLUTO.shp
	ogr2ogr -f "ESRI Shapefile" Queens_buffered.shp Queens.shp -dialect sqlite -overwrite -sql "select *, ST_Buffer(Geometry, 0.0001) as Geometry from Queens" -nlt GEOMETRY 
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/parcels/Queens.shp raw/MapPLUTO/Queens/QNMapPLUTO.shp
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/parcels/Staten_Island.shp raw/MapPLUTO/Staten_Island/SIMapPLUTO.shp

download_nycha:
	mkdir -p raw/nycha
	curl -L "https://data.cityofnewyork.us/api/geospatial/i9rv-hdr5?method=export&format=Shapefile" -o raw/nycha/nycha.zip
	unzip raw/nycha/nycha.zip -d raw/nycha

process_nycha: prepare_processed
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/nycha/nycha.shp $(wildcard raw/nycha/*.shp)

download_postoffices:
	mkdir -p raw/postoffices
	curl -L "https://github.com/nycommons/nyc-post-offices/raw/master/data/shp/nyc-post-offices.zip" -o raw/postoffices/postoffices.zip
	unzip raw/postoffices/postoffices.zip -d raw/postoffices

process_postoffices:
	mkdir -p processed/postoffices
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/postoffices/postoffices.shp $(wildcard raw/postoffices/*.shp)

download_libraries:
	mkdir -p raw/libraries
	curl -L "https://github.com/nycommons/nyc-libraries/raw/master/data/shp/nyc-libraries.zip" -o raw/libraries/libraries.zip
	unzip raw/libraries/libraries.zip -d raw/libraries

process_libraries: prepare_processed
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/libraries/libraries.shp $(wildcard raw/libraries/*.shp)

download_waterfront:
	mkdir -p raw/waterfront
	curl -L "https://github.com/nycommons/nyc-public-waterfront/raw/master/data/shp/nyc-public-waterfront.zip" -o raw/waterfront/waterfront.zip
	unzip raw/waterfront/waterfront.zip -d raw/waterfront

process_waterfront:
	mkdir -p processed/waterfront
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/waterfront/waterfront.shp $(wildcard raw/waterfront/*.shp)

download_citycouncilmembers:
	mkdir -p processed/citycouncilmembers
	curl -L "https://data.cityofnewyork.us/api/views/uvw5-9znb/rows.csv?accessType=DOWNLOAD" -o processed/citycouncilmembers/citycouncilmembers.csv

download_communitydistrictsdetails:
	mkdir -p processed/communitydistrictsdetails
	curl -L "https://morph.io/ebrelsford/nyc_community_boards/data.csv?key=vHPPJAEqTatkpXdpMF%2FC&query=select+%2A+from+%27community_boards%27" -o processed/communitydistrictsdetails/communitydistrictsdetails.csv

download_parks:
	mkdir -p raw/parks
	curl -L "https://data.cityofnewyork.us/api/geospatial/rjaj-zgq7?method=export&format=Shapefile" -o raw/parks/parks.zip
	unzip raw/parks/parks.zip -d raw/parks

process_parks:
	mkdir -p processed/parks
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/parks/parks.shp $(wildcard raw/parks/*.shp)

download_landmarks:
	mkdir -p raw/landmarks
	curl -L "https://data.cityofnewyork.us/api/geospatial/ch5p-r223?method=export&format=Shapefile" -o raw/landmarks/landmarks.zip
	unzip raw/landmarks/landmarks.zip -d raw/landmarks

process_landmarks: prepare_processed
	mkdir -p processed/landmarks
	ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -overwrite processed/landmarks/landmarks.shp $(wildcard raw/landmarks/*.shp)
