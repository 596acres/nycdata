#
# Save pictures from database to a csv
#
SQL="SELECT l.bbl, p.picture, p.added, '\"' || REPLACE(REPLACE(p.description, '\"', E'\"\"'), ',', E'\\,') || '\"' AS description FROM lots_lot l INNER JOIN organize_picture p ON p.lot_id = l.id;"

DB_NAME=ebrelsford_fns
DB_USER=ebrelsford_fns

psql -U $DB_USER $DB_NAME -F "," --no-align -c "$SQL" | head -n -1 > pictures.csv


#
# Archive the actual pictures
#
PICTURES_DIR=$HOME/webapps/596acres_django/fiveninesix/media/pictures/
DATA_DIR=`pwd`

cd $PICTURES_DIR && tar czf $DATA_DIR/pictures.tar.gz *
