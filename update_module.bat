@echo off
set MODULE=%1

docker exec -it tresvance_odoo19 odoo -c /etc/odoo/odoo.conf -u %MODULE% -d tresvance_dev --stop-after-init
docker restart tresvance_odoo19

pause