#!/bin/sh
mysql -ushu -plee2000 -hlocalhost -e "DROP SCHEMA finance;";
mysql -ushu -plee2000 -hlocalhost -e "CREATE SCHEMA finance DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;"
#python manage.py syncdb --noinput
python manage.py syncdb
#python manage.py add_function
