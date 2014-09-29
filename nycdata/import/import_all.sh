DATA_DIR=../raw/
DB_NAME=llnyc
DB_USER=llnyc

psql -U $DB_USER $DB_NAME -F "," --no-align -c "TRUNCATE lots_lot CASCADE; TRUNCATE lots_lotgroup CASCADE; TRUNCATE owners_owner CASCADE; TRUNCATE steward_stewardproject CASCADE; TRUNCATE lots_lotlayer CASCADE; TRUNCATE notes_note CASCADE; TRUNCATE organize_organizer CASCADE; TRUNCATE livinglots_lots_use CASCADE;"

django-admin loadlots $DATA_DIR/lots.csv
django-admin loadlotgroups $DATA_DIR/lotgroups.csv
django-admin loadowners $DATA_DIR/owners.csv
django-admin loadstewards $DATA_DIR/stewards.csv
django-admin loadorganizers $DATA_DIR/organizers.csv
django-admin loadwatchers $DATA_DIR/watchers.csv
django-admin loadnotes $DATA_DIR/notes.csv
