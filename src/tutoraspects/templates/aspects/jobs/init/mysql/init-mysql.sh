echo "Initialising MySQL..."
mysql_connection_max_attempts=10
mysql_connection_attempt=0
until mysql -u {{ MYSQL_ROOT_USERNAME }} --password="{{ MYSQL_ROOT_PASSWORD }}" --host "{{ MYSQL_HOST }}" --port {{ MYSQL_PORT }} -e 'exit'
do
    mysql_connection_attempt=$(expr $mysql_connection_attempt + 1)
    echo "    [$mysql_connection_attempt/$mysql_connection_max_attempts] Waiting for MySQL service (this may take a while)..."
    if [ $mysql_connection_attempt -eq $mysql_connection_max_attempts ]
    then
      echo "MySQL initialisation error" 1>&2
      exit 1
    fi
    sleep 10
done
echo "MySQL is up and running"

# Superset MySQL database, by default points to the same host as edx-platform
mysql -u {{ MYSQL_ROOT_USERNAME }} --password="{{ MYSQL_ROOT_PASSWORD }}" --host "{{ MYSQL_HOST }}" --port {{ MYSQL_PORT }} -e "CREATE DATABASE IF NOT EXISTS {{ SUPERSET_DB_NAME }} /*!40100 DEFAULT CHARACTER SET utf8mb4 */;"

# Superset system user
mysql -u {{ MYSQL_ROOT_USERNAME }} --password="{{ MYSQL_ROOT_PASSWORD }}" --host "{{ MYSQL_HOST }}" --port {{ MYSQL_PORT }} -e "CREATE USER IF NOT EXISTS '{{ SUPERSET_DB_USERNAME }}';"
mysql -u {{ MYSQL_ROOT_USERNAME }} --password="{{ MYSQL_ROOT_PASSWORD }}" --host "{{ MYSQL_HOST }}" --port {{ MYSQL_PORT }} -e "ALTER USER '{{ SUPERSET_DB_USERNAME }}'@'%' IDENTIFIED BY '{{ SUPERSET_DB_PASSWORD }}';"
mysql -u {{ MYSQL_ROOT_USERNAME }} --password="{{ MYSQL_ROOT_PASSWORD }}" --host "{{ MYSQL_HOST }}" --port {{ MYSQL_PORT }} -e "GRANT ALL ON {{ SUPERSET_DB_NAME }}.* TO '{{ SUPERSET_DB_USERNAME }}'@'%';"
