export PGPASSWORD=root
psql -h localhost -d Blockbuster -U postgres -p 5432 -a -q -f ./scripts/main.sql