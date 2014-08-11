#!/bin/sh
echo -n "Enter app name to backup > "
read input
rm $input/fixtures/initial_data.json
python manage.py dumpdata --natural --format=json $input > $input/fixtures/initial_data.json
echo "App $input has been successfully backed up at $input/fixtures/initial_data.json"
