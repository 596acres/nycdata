SQL="SELECT l.bbl, '\"' || REPLACE(REPLACE(n.noter, '\"', E'\\\"'), ',', E'\\,') || '\"' AS added_by_name, n.added, '\"' || REPLACE(REPLACE(n.text, '\"', E'\"\"'), ',', E'\\,') || '\"' AS text FROM lots_lot l INNER JOIN organize_note n ON n.lot_id = l.id;"

DB_NAME=ebrelsford_fns
DB_USER=ebrelsford_fns

psql -U $DB_USER $DB_NAME -F "," --no-align -c "$SQL" | head -n -1 > notes.csv
