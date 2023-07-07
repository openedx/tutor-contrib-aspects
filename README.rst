The Aspects plugin for Tutor
============================

Aspects Learner Analytics combines several free, open source, tools to add analytics and reporting capabilities to the Open edX platform. This plugin offers easy installation, configuration, and deployment of these tools using `Tutor <https://docs.tutor.overhang.io>`__. The tools Aspects uses are:

- `ClickHouse <https://clickhouse.com>`__, a fast, scalable analytics database that can be run anywhere
- `Apache Superset <https://superset.apache.org>`__, a data visualization platform and data API
- `OpenFUN Ralph <https://https://openfun.github.io/ralph/>`__, a Learning Record store (and more) that can validate and store xAPI statements in ClickHouse
- `Vector <https://vector.dev/>`__, a log forwarding tool that can be used to forward tracking log and xAPI data to ClickHouse
- `event-routing-backends <https://https://event-routing-backends.readthedocs.io/en/latest/>`__, an Open edX plugin that transforms tracking logs into xAPI and optionally forwards them to one or more Learning Record Stores in near real time
- `event-sink-clickhouse <https://github.com/openedx/openedx-event-sink-clickhouse>`__, an Open edX plugin that exports course structure and high level data to ClickHouse at publish time
- `dbt <https://www.getdbt.com/>`__, a tool to build data pipelines from SQL queries. The dbt project used by this plugin is `aspects-dbt <https://github.com/openedx/aspects-dbt>`__.

See https://github.com/openedx/openedx-oars for more details about the Aspects architecture and high level documentation.

Aspects is a community developed effort combining the Cairn project by Overhang.io and the OARS project by EduNEXT, OpenCraft, and Axim Collaborative.

Note: Aspects is in heavy development and not yet production ready! Please feel
free to experiment with the system and offer feedback about what you'd like to see
by adding Issues in this repository.

Compatibility
-------------

This plugin is compatible with Tutor 15.0.0 and later and is expected to be compatible with Open edX releases from Nutmeg forward.

Installation
------------

The Aspects project can be installed in a Tutor environment with the following command

::

    pip install git+https://github.com/openedx/tutor-contrib-aspects


Usage
-----

#. Enable the plugins::

    tutor plugins enable aspects

#. Save the changes to the environment::

    tutor config save

#. Because we're installing a new app in LMS (event-routing-backends) you will need to
   rebuild your openedx image::

    tutor images build openedx

#. Run the initialization scripts in your chosen environment (dev or local)::

    tutor [dev|local] do init

#. (Optional) Load test xAPI data into Ralph/Clickhouse/Superset (with ``--help`` for usage)::

    tutor [dev|local] do load-xapi-test-data


Superset Assets
---------------

Aspects maintains the Superset assets in this repository, specifically the dashboards,
charts, datasets, and databases. That means that any updates made here will be reflected
on your Superset instance when you update your deployment.

But it also means that any local changes you make to these assets will be overwritten
when you update your deployment. To prevent your local changes from being overwritten,
please create new assets and make your changes there instead. You can copy an existing
asset by editing the asset in Superset and selecting "Save As" to save it to a new name.

Define your own superset assets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To programatically define custom superset assets there is a patch you can use with an
inline plugin. The patch ``superset-extra-assets`` will allow you to define your
own superset assets in a yaml file and have them automatically imported into superset
when you run ``tutor [dev|local|k8s] init -l aspects``.

An example of this patch is provided as reference:

..  code-block:: yaml

    name: custom-inline-plugin
    version: 0.1.0
    patches:
    superset-extra-assets: |
        - _file_name: my-dashboard.yaml
          dashboard_title: "..."
          ...
        - _file_name: my-chart.yaml
          slice_name: "..."
          ...
        - _file_name: my-database.yaml
          database_name: "..."
          ...
        - _file_name: my-dataset.yaml
          table_name: "..."
          ...

The patch is expected to be a list of assets with an extra attribute called ``file_name`` , which uniquely identifies the asset entry. This file does not need to exist anywhere; it will be created with the rest of the yaml in that stanza as part of the init process. Each asset is expected to be a valid yaml file with the attributes that superset expects for each asset type. See `assets.yaml`_ for examples of asset yaml declarations.

The tutor command will generate a .yaml file with the content of an exported zip file. This is useful if you want to add a new asset to the default assets provided by Aspects. You can then edit the generated file and add it to the patch above.

..  code-block:: sh

    tutor aspects serialize file.zip

Override superset default assets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to override the default assets provided by Aspects you can do so by using the
patch defined above and make sure that the uuid of the asset you are overriding matches
the one in the default assets. You can find the uuid of the default assets in the
default `assets.yaml`_ file.

.. _assets.yaml: tutoraspects/templates/aspects/apps/superset/pythonpath/assets.yaml


Sharing Charts and Dashboards
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To share your charts with others in the community, use Superset's "Export" button to
save a zip file of your charts and related datasets.

.. note::
    The exported datasets will contain hard-coded references to your particular
    databases, including your database hostname, port, and username, but it
    will not contain passwords.

To import charts or dashboards shared by someone in the community:

#. Expand the zip file and look for any files added under ``databases``.
   Update the ``sqlalchemy_uri`` to match your database's connection details.
#. Compress the files back into a ``.zip`` file.
#. On the Charts or Dashboards page, use the "Import" button to upload your ``.zip`` file.


Contributing Charts and Dashboards to Aspects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Superset assets provided by Aspects can be found in the templated `assets.yaml`_ file.
For the most part, these files what Superset exports, but with some crucial differences
which make these assets usable across all Tutor deployments.

To contribute assets to Aspects:

#. Export the assets you want to contribute as described in `Sharing Charts and Dashboards`
#. Expand the ``.zip`` file.
#. Update any database connection strings to use Tutor configuration template variables
   instead of hard-coded strings, e.g. replace ``clickhouse`` with ``{{CLICKHOUSE_HOST}}``.
   Passwords can be left as ``{{CLICKHOUSE_PASSWORD}}``, though be aware that if you are adding new
   databases, you'll need to update ``SUPERSET_DB_PASSWORDS`` in the init scripts.
   Here is the default connection string for reference::

    ``clickhousedb+connect://{{CLICKHOUSE_REPORT_URL}}``
#. Remove any ``metadata.yaml`` files from the export. We generate these as needed during import.
#. Merge your exported files into the directories and files in the `assets.yaml`_.
#. Submit a PR with screenshots of your new chart or dashboards, along with an explanation
   of what data question they answer.


Virtual datasets in Superset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Superset supports creating virtual datasets, which are datasets defined using a SQL query instead of mapping directly to an underlying database object. Aspects leverages virtual datasets, along with `SQL templating <https://superset.apache.org/docs/installation/sql-templating/>`_, to make better use of table indexes.

To make it easier for developers to manage virtual datasets, there is an extra step that can be done on the output of ``tutor aspects serialize``. The ``sql`` section of the dataset yaml can be moved to its own file in the `queries`_ directory and included in the yaml like so:

.. code-block:: yaml

   sql: "{% include 'openedx-assets/queries/query.sql' %}"


However, please keep in mind that the assets declaration is itself a jinja template. That means that any jinja used in the dataset definition should be escaped. There are examples of how to handle this in the existing queries, such as `dim_courses.sql`_.

.. _queries: tutoraspects/templates/aspects/apps/superset/pythonpath/queries

.. _dim_courses.sql: tutoraspects/templates/aspects/apps/superset/pythonpath/queries/dim_courses.sql


Changing Superset Language Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Superset localization is a work in progress, but you can change the default language and set alternate languages from the currently supported list by changing the Tutor configuration variables:

Default language: ``tutor config save --set SUPERSET_DEFAULT_LOCALE=en``

Available languages are stored in a mapping, and so best edited directly in Tutor's config.yml file. You can find the path to the config file with ``tutor config printroot``. Once there, you can set the SUPERSET_SUPPORTED_LANGUAGES with a mapping of the following structure::

    SUPERSET_SUPPORTED_LANGUAGES: {
        "en": {"flag": "us", "name": "English"},
        "es": {"flag": "es", "name": "Spanish"},
        "it": {"flag": "it", "name": "Italian"},
        "fr": {"flag": "fr", "name": "French"},
        "zh": {"flag": "cn", "name": "Chinese"},
        "ja": {"flag": "jp", "name": "Japanese"},
        "de": {"flag": "de", "name": "German"},
        "pt": {"flag": "pt", "name": "Portuguese"},
        "pt_BR": {"flag": "br", "name": "Brazilian Portuguese"},
        "ru": {"flag": "ru", "name": "Russian"},
        "ko": {"flag": "kr", "name": "Korean"},
        "sk": {"flag": "sk", "name": "Slovak"},
        "sl": {"flag": "si", "name": "Slovenian"},
        "nl": {"flag": "nl", "name": "Dutch"},
    }

Where the first key is the abbreviation of the language to use, "flag" is which flag icon is displayed in the user interface for choosing the language, and "name" is the displayed name for that language. The mapping above shows all of the current languages supported by Superset, but please note that different languages have different levels of completion and support at this time.


Extending the DBT project
^^^^^^^^^^^^^^^^^^^^^^^^^^

To extend the DBT project there are multiple options:

    #. DBT_REPOSITORY: A git repository URL to the DBT project
    #. DBT_BRANCH: A git branch to use for the DBT project
    #. DBT_REPOSITORY_PATH: A path to the DBT project in the git repository
    #. EXTRA_DBT_PACKAGES: A list of python packages necessary for the DBT project
    #. DBT_ENABLE_OVERRIDE: A boolean to enable/disable the DBT project override, those overrides
       allows you to extend the DBT project without having to fork it. For this to work you need
       to create a patch with the name ``dbt-packages`` and ``dbt-project``. We recommend to copy
       the default DBT files (``dbt_project.yml`` and ``packages.yml``) and add your changes from
       there.


Running Clickhouse queries at startup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run extra SQL queries at startup you can use the tutor patch ``clickhouse-extra-sql``.:

..  code-block:: yaml

    clickhouse-extra-sql: |
        SELECT * from {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_XAPI_TABLE}} LIMIT 1;

License
-------

This software is licensed under the terms of the AGPLv3.
