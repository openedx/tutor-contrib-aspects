#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Modified from original:
#
# https://github.com/apache/superset/blob/969c963/docker/docker-init.sh

set -e

STEP_CNT=5

echo_step() {
cat <<EOF

######################################################################


Init Step ${1}/${STEP_CNT} [${2}] -- ${3}


######################################################################

EOF
}
# Initialize the database
echo_step "1" "Starting" "Applying DB migrations"
superset db upgrade
superset init
echo_step "1" "Complete" "Applying DB migrations"

# Create an admin user
echo_step "2" "Starting" "Setting up admin user"
superset fab create-admin \
  --username "{{ SUPERSET_ADMIN_USERNAME }}" \
  --password "{{ SUPERSET_ADMIN_PASSWORD }}" \
  --firstname Superset \
  --lastname Admin \
  --email "{{ SUPERSET_ADMIN_EMAIL }}"

superset fab create-admin \
  --username "{{ SUPERSET_LMS_USERNAME }}" \
  --password "{{ SUPERSET_LMS_PASSWORD }}" \
  --firstname LMS \
  --lastname Admin \
  --email "{{ SUPERSET_LMS_EMAIL }}"

# Update the password of the Admin user
# (in case it changed since the user was created)
superset fab reset-password \
  --username "{{ SUPERSET_ADMIN_USERNAME }}" \
  --password "{{ SUPERSET_ADMIN_PASSWORD }}"
echo_step "2" "Complete" "Setting up admin user"

# Create default roles and permissions
echo_step "3" "Starting" "Setting up roles and perms"
superset fab import-roles -p /app/security/roles.json
echo_step "3" "Complete" "Setting up roles and perms"

echo_step "4" "Starting" "Importing assets"

bash /app/scripts/import-assets.sh

echo_step "4" "Complete" "Importing assets"
