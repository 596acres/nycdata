DB_NAME=ebrelsford_fns
DB_USER=ebrelsford_fns

SQL="SELECT l.bbl, '\"' || oc.name || '\"' AS name, '\"' || o.name || '\"' AS owner_name, oc.phone, oc.email, oc.jurisdiction, '\"' || REPLACE(REPLACE(oc.notes, '\"', E'\\\"'), ',', E'\\,') || '\"' AS notes FROM lots_lot l INNER JOIN lots_ownercontact oc ON l.owner_contact_id = oc.id INNER JOIN lots_owner o ON oc.owner_id = o.id;"

psql -U $DB_USER $DB_NAME -F "," --no-align -c "$SQL" | head -n -1 > ownercontacts.csv
