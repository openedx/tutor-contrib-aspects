OARS plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This plugin controls the configuration of several different other Tutor plugins
to join them into the Open edx "Open Analytics Reference System", a way for Open
edX installs to collect and display learner data in a consistent way.

See https://github.com/openedx/openedx-oars for more details.

Installation
------------

The OARS system relies on several Tutor plugins:

::

    pip install git+https://github.com/openedx/tutor-contrib-oars
    pip install git+https://github.com/openedx/tutor-contrib-ralph
    pip install git+https://github.com/openedx/tutor-contrib-clickhouse
    pip install git+https://github.com/openedx/tutor-contrib-superset


See these repos for more information.

Usage
-----

1. Enable the plugins::

    tutor plugins enable oars
    tutor plugins enable ralph
    tutor plugins enable clickhouse
    tutor plugins enable superset

2. Save the changes to the environment::

    tutor config save

3. Run the initialization scripts in your chosen environment (dev or local)::

    tutor [dev|local] do init

4. (Optional) Load test xAPI data into Ralph/Clickhouse/Superset (with ``--help`` for usage)::

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

1. Expand the zip file and look for any files added under ``databases``.
   Update the ``sqlalchemy_uri`` to match your database's connection details.
1. Compress the files back into a ``.zip`` file.
1. On the Charts or Dashboards page, use the "Import" button to upload
   your ``.zip`` file.


Contributing Charts and Dashboards to OARS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Superset assets provided by OARS can be found in the templated `assets directory`_. For the most part, these files what Superset exports, but with some crucial differences which make these assets usable across all Tutor deployments.

To contribute assets to OARS:

#. Export the assets you want to contribute as described in :ref:`Sharing Charts and Dashboards`
#. Expand the ``.zip`` file.
#. Update any database connection strings to use Tutor configuration template variables instead of hard-coded strings, e.g. replace ``mysql`` with ``{{MYSQL_HOST}}``.
   Passwords can be left as ``XXXXXXXX``, though be aware that if you are adding new databases, you'll need to update ``SUPERSET_DB_PASSWORDS`` in the init scripts.
#. Remove any ``metadata.yaml`` files from the export. We generate these as needed during import.
#. Merge your exported files into the directories and files in the `assets directory`_.
#. Submit a PR with screenshots of your new chart or dashboards, along with an explanation of what data question they answer.

.. _assets directory: https://github.com/openedx/tutor-contrib-oars/tree/main/tutoroars/templates/oars/apps/data/assets


License
-------

This software is licensed under the terms of the AGPLv3.
