echo "MySQL init after Superset migrations..."

# Grant SELECT access to a subset of superset metadata tables
for TABLE in ab_user dashboards logs slices tables; do
    mysql -u {{ MYSQL_ROOT_USERNAME }} --password="{{ MYSQL_ROOT_PASSWORD }}" --host "{{ MYSQL_HOST }}" --port {{ MYSQL_PORT }} -e "GRANT SELECT ON {{ SUPERSET_DB_METADATA_NAME }}.${TABLE} TO '{{ SUPERSET_DB_USERNAME }}'@'%';"
done
