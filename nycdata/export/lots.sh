# Associate everything by BBL

# Handle all foreign keys separately:
#  group with access
#  lot groups
#  owners
#  owner contacts
SQL="SELECT address, borough, bbl, block, lot, zipcode, ST_AsText(centroid) AS centroid, centroid_source, is_vacant, actual_use, accessible, name FROM lots_lot;"
DB_NAME=ebrelsford_fns
DB_USER=ebrelsford_fns

psql -U $DB_USER $DB_NAME -F "\",\"" --no-align -c "$SQL" | sed "s/^/\"/; s/$/\"/" | head -n -1 > lots.csv
