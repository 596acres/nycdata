SQL="SELECT l.bbl, '\"' || w.name || '\"' AS name, w.phone, w.email, w.added, w.email_hash FROM organize_watcher w LEFT OUTER JOIN lots_lot l ON l.id = w.lot_id;"
DB_NAME=ebrelsford_fns
DB_USER=ebrelsford_fns

psql -U $DB_USER $DB_NAME -F "," --no-align -c "$SQL" | head -n -1 > watchers.csv
