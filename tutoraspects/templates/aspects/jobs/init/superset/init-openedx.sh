# Create a DOT applicaton so Superset can use Open edX authenticatioon
./manage.py lms manage_user superset superset@apache
./manage.py lms create_dot_application \
    --grant-type authorization-code \
    --redirect-uris "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ SUPERSET_HOST }}/oauth-authorized/openedxsso" \
    --client-id {{ SUPERSET_OAUTH2_CLIENT_ID }} \
    --client-secret {{ SUPERSET_OAUTH2_CLIENT_SECRET }} \
    --scopes "user_id" \
    --update \
    superset-sso superset
./manage.py lms create_dot_application \
    --grant-type authorization-code \
    --redirect-uris "http://{{ SUPERSET_HOST }}:{{SUPERSET_PORT}}/oauth-authorized/openedxsso" \
    --client-id {{ SUPERSET_OAUTH2_CLIENT_ID_DEV }} \
    --client-secret {{ SUPERSET_OAUTH2_CLIENT_SECRET }} \
    --scopes "user_id" \
    --update \
    superset-sso-dev superset
