#!/usr/bin/env bash
set -e

#
# Always install local overrides first
#
/usr/bin/env bash /app/docker/docker-bootstrap.sh

# Create an admin user
echo "Setting up admin user"
superset fab create-admin \
  --username "{{ SUPERSET_ADMIN_USERNAME }}" \
  --password "{{ SUPERSET_ADMIN_PASSWORD }}" \
  --firstname Superset \
  --lastname Admin \
  --email "{{ SUPERSET_ADMIN_EMAIL }}"
echo "Setting up admin user...Complete"

# Update the password of the Admin user
# (in case it changed since the user was created)
echo "Resetting password for admin user"
superset fab reset-password \
  --username "{{ SUPERSET_ADMIN_USERNAME }}" \
  --password "{{ SUPERSET_ADMIN_PASSWORD }}"
echo "Resetting password for admin user...Complete"
