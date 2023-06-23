cat > /tmp/erb_config.json <<EOF
{
  "model": "event_routing_backends.RouterConfiguration",
  "data":
  [
    {
      "enabled": true,
      "backend_name": "xAPI",
    "route_url": "{% if RUN_RALPH %}http://ralph:{{ RALPH_PORT }}{% else %}{% if RALPH_RUN_HTTPS %}https://{% else %}http://{% endif %}{{ RALPH_HOST }}{% endif %}/xAPI/",
      "auth_scheme": "Basic",
      "username": "{{ RALPH_LMS_USERNAME }}",
      "password": "{{ RALPH_LMS_PASSWORD }}"
    }
  ]
}
EOF

./manage.py lms manage_user tutor-contrib-aspects aspects@axim --unusable-password
./manage.py lms populate_model -f /tmp/erb_config.json -u tutor-contrib-aspects
