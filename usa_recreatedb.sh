#!/bin/sh
mysql -ushu -plee2000 -hlocalhost -e "DROP SCHEMA finance_usa;";
mysql -ushu -plee2000 -hlocalhost -e "CREATE SCHEMA finance_usa DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;"
#python manage.py syncdb --noinput
python manage.py syncdb
#python manage.py add_function
