#!/bin/bash

MODULE=$1
DB=tresvance_dev

echo "Updating module: $MODULE"

docker exec -i tresvance_odoo19 odoo -c /etc/odoo/odoo.conf -u $MODULE -d $DB --stop-after-init

echo "Restarting Odoo..."

docker restart tresvance_odoo19

echo "Done!"