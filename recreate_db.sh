#!/bin/sh
mysql -uroot -paiwahc1F -hdb-writer -e "DROP SCHEMA taishan;";
mysql -uroot -paiwahc1F -hdb-writer -e "CREATE SCHEMA taishan DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;";
python manage.py syncdb --noinput
python manage.py add_function
