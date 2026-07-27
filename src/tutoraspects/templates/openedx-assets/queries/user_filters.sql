{% raw -%}

{% if filter_values("username") != [] or filter_values(
    "name"
) != [] or filter_values("email") != [] %}
    and actor_id in (
        select external_user_id::String
        from {% endraw -%} {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii{%- raw %}
        where
            1 = 1
            {% if filter_values("username") != [] %}
                and username in {{ filter_values("username") | where_in }}
            {% endif %}
            {% if filter_values("name") != [] %}
                and name in {{ filter_values("name") | where_in }}
            {% endif %}
            {% if filter_values("email") != [] %}
                and email in {{ filter_values("email") | where_in }}
            {% endif %}
    )
{% endif %}

{%- endraw %}
