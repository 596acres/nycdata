SQL="SELECT l.bbl, l2.bbl AS parent FROM lots_lot l LEFT OUTER JOIN lots_lot l2 ON l.parent_lot_id = l2.id WHERE l.parent_lot_id IS NOT NULL;"

DB_NAME=ebrelsford_fns
DB_USER=ebrelsford_fns

psql -U $DB_USER $DB_NAME -F "," --no-align -c "$SQL" | head -n -1 > lotgroups.csv
