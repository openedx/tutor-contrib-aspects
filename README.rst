OARS plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This plugin controls the configuration of several different other Tutor plugins
to join them into the Open edx "Open Analytics Reference System", a way for Open
edX installs to collect and display learner data in a consistent way.

See https://github.com/openedx/openedx-oars for more details.

Note: OARS is in early development and not at all production ready! Please feel free to experiment with the system and offer feedback about what you'd like to see!

Compatibility
-------------

This plugin is compatible with Tutor 15.0.0 and later.

Installation
------------

The OARS system relies on several Tutor plugins currently. They are in the process of being consolidated into tutor-contrib-oars, so these steps should be simplified shortly.

::

    pip install git+https://github.com/openedx/tutor-contrib-oars
    pip install git+https://github.com/openedx/tutor-contrib-ralph
    pip install git+https://github.com/openedx/tutor-contrib-superset


See these repos for more information.

Usage
-----

#. Enable the plugins::

    tutor plugins enable oars
    tutor plugins enable ralph
    tutor plugins enable superset

#. Save the changes to the environment::

    tutor config save

#. Because we're installing a new app in LMS (event-routing-backends) you will need to rebuild your openedx image::

    tutor images build openedx

#. Run the initialization scripts in your chosen environment (dev or local)::

    tutor [dev|local] do init

#. (Optional) Load test xAPI data into Ralph/Clickhouse/Superset (with ``--help`` for usage)::

    tutor [dev|local] do load-xapi-test-data


Superset Assets
---------------

OARS maintains the Superset assets in this repository, specifically the dashboards, charts, datasets, and databases. That means that any updates made here will be reflected on your Superset instance when you update your deployment.

But it also means that any local changes you make to these assets will be overwritten when you update your deployment. To prevent your local changes from being overwritten, please create new assets and make your changes there instead. You can copy an existing asset by editing the asset in Superset and selecting "Save As" to save it to a new name.

Sharing Charts and Dashboards
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To share your charts with others in the community, use Superset's "Export" button to save a zip file of your charts and related datasets.

.. note::
    The exported datasets will contain hard-coded references to your particular
    databases, including your database hostname, port, and username, but it
    will not contain passwords.

To import charts or dashboards shared by someone in the community:

#. Expand the zip file and look for any files added under ``databases``.
   Update the ``sqlalchemy_uri`` to match your database's connection details.
#. Compress the files back into a ``.zip`` file.
#. On the Charts or Dashboards page, use the "Import" button to upload your ``.zip`` file.


Contributing Charts and Dashboards to OARS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Superset assets provided by OARS can be found in the templated `assets directory`_. For the most part, these files what Superset exports, but with some crucial differences which make these assets usable across all Tutor deployments.

To contribute assets to OARS:

#. Export the assets you want to contribute as described in `Sharing Charts and Dashboards`
#. Expand the ``.zip`` file.
#. Update any database connection strings to use Tutor configuration template variables instead of hard-coded strings, e.g. replace ``mysql`` with ``{{MYSQL_HOST}}``.
   Passwords can be left as ``XXXXXXXX``, though be aware that if you are adding new databases, you'll need to update ``SUPERSET_DB_PASSWORDS`` in the init scripts.
#. Remove any ``metadata.yaml`` files from the export. We generate these as needed during import.
#. Merge your exported files into the directories and files in the `assets directory`_.
#. Submit a PR with screenshots of your new chart or dashboards, along with an explanation of what data question they answer.

.. _assets directory: https://github.com/openedx/tutor-contrib-oars/tree/main/tutoroars/templates/oars/apps/data/assets


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

License
-------

This software is licensed under the terms of the AGPLv3.
