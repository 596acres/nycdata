#!/bin/bash
set -e
set -o errexit

DATA_DIR=../raw/
DB_NAME=llnyc
DB_USER=llnyc

psql -U $DB_USER $DB_NAME -F "," --no-align -c "TRUNCATE actstream_action CASCADE; TRUNCATE lots_lot CASCADE; TRUNCATE lots_lotgroup CASCADE; TRUNCATE owners_owner CASCADE; TRUNCATE owners_ownercontact CASCADE; TRUNCATE steward_stewardproject CASCADE; TRUNCATE lots_lotlayer CASCADE; TRUNCATE notes_note CASCADE; TRUNCATE livinglots_organize_organizertype CASCADE; TRUNCATE organize_organizer CASCADE; TRUNCATE livinglots_lots_use CASCADE; TRUNCATE photos_photo CASCADE;" 

django-admin loadlots $DATA_DIR/lots.csv
django-admin loadlotgroups $DATA_DIR/lotgroups.csv
django-admin loadowners $DATA_DIR/owners.csv
django-admin loadownercontacts $DATA_DIR/ownercontacts.csv
django-admin loadstewards $DATA_DIR/stewards.csv
django-admin loadnotes $DATA_DIR/notes.csv
django-admin loadpictures $DATA_DIR/pictures.csv $DATA_DIR/pictures.tar.gz
django-admin loadorganizers $DATA_DIR/organizers.csv
django-admin loadwatchers $DATA_DIR/watchers.csv

django-admin finishlots
