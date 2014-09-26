SQL="SELECT l.bbl, '\"' || o.name || '\"' AS name, o.phone, o.email, o.url, ot.name AS type, ot.is_group, '\"' || REPLACE(REPLACE(o.notes, '\"', E'\"\"'), ',', E'\\,') || '\"' AS notes, o.facebook_page, o.added, o.email_hash FROM organize_organizer o LEFT OUTER JOIN lots_lot l ON l.id = o.lot_id LEFT OUTER JOIN organize_organizertype ot ON ot.id = o.type_id;"
DB_NAME=ebrelsford_fns
DB_USER=ebrelsford_fns

psql -U $DB_USER $DB_NAME -F "," --no-align -c "$SQL" | head -n -1 > organizers.csv
