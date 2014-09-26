DB_NAME=ebrelsford_fns
DB_USER=ebrelsford_fns

SQL="SELECT l.bbl, '\"' || o.name || '\"' AS name, o.phone, t.name AS type, o.code, '\"' || o.person || '\"' AS person, o.site, o.email, o.oasis_name, '\"' || REPLACE(REPLACE(o.notes, '\"', E'\\\"'), ',', E'\\,') || '\"' AS notes FROM lots_lot l LEFT JOIN lots_owner o ON l.owner_id = o.id LEFT JOIN lots_ownertype t ON t.id = o.type_id;"

psql -U $DB_USER $DB_NAME -F "," --no-align -c "$SQL" | head -n -1 > owners.csv
