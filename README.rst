The Aspects plugin for Tutor
============================

Aspects Learner Analytics combines several free, open source, tools to add analytics and reporting capabilities to the Open edX platform. This plugin offers easy installation, configuration, and deployment of these tools using `Tutor <https://docs.tutor.overhang.io>`__. The tools Aspects uses are:

- `ClickHouse <https://clickhouse.com>`__, a fast, scalable analytics database that can be run anywhere
- `Apache Superset <https://superset.apache.org>`__, a data visualization platform and data API
- `OpenFUN Ralph <https://openfun.github.io/ralph/>`__, a Learning Record store (and more) that can validate and store xAPI statements in ClickHouse
- `Vector <https://vector.dev/>`__, a log forwarding tool that can be used to forward tracking log and xAPI data to ClickHouse
- `event-routing-backends <https://event-routing-backends.readthedocs.io/en/latest/>`__, an Open edX plugin that transforms tracking logs into xAPI and optionally forwards them to one or more Learning Record Stores in near real time
- `event-sink-clickhouse <https://github.com/openedx/openedx-event-sink-clickhouse>`__, an Open edX plugin that exports course structure and high level data to ClickHouse at publish time
- `dbt <https://www.getdbt.com/>`__, a tool to build data pipelines from SQL queries. The dbt project used by this plugin is `aspects-dbt <https://github.com/openedx/aspects-dbt>`__.

See https://github.com/openedx/openedx-aspects for more details about the Aspects architecture and high level documentation.

Aspects is a community developed effort combining the Cairn project by Overhang.io and the OARS project by EduNEXT, OpenCraft, and Axim Collaborative.

Note: Aspects is beta and not yet production ready! Please feel free to experiment with the system and offer feedback about what you'd like to see by adding Issues in this repository. Current details on the beta progress can be found here: https://openedx.atlassian.net/wiki/spaces/COMM/pages/3861512203/Aspects+Beta

Compatibility
-------------

This plugin is compatible with Tutor 15.0.0 and later and is expected to be compatible with Open edX releases from Nutmeg forward.

Installation
------------

Aspects is implemented as a Tutor plugin. Documentation will be coming soon to cover how to install Aspects in non-Tutor environments, but by far the easiest way to try and install it is via Tutor. These instructions assume you are running a `tutor local` install, which is the fastest and easiest way to get started.

#. Install Tutor: https://docs.tutor.overhang.io/install.html#install

#. Create an admin user on the LMS: https://docs.tutor.overhang.io/whatnext.html#logging-in-as-administrator

#. Install the Aspects plugin (in your Tutor Python environment)::

    pip install tutor-contrib-aspects

#. Enable the plugins::

    tutor plugins enable aspects

#. Save the changes to the environment::

    tutor config save

#. Because we're installing new applications in LMS (event-routing-backends, event-sink-clickhouse) you will need to rebuild your openedx image::

    tutor images build openedx --no-cache

#. Run the initialization scripts::

    tutor local do init

At this point you should have a working Tutor / Aspects environment, but with no way to create data! There are a few options for how to proceed.

#. If you would just like to see some data populated in the charts without loading a real course in the LMS you can create test data in the database (use ``--help`` for usage)::

        tutor local do load-xapi-test-data

#. OR Load the test course and generate real data from the LMS:

   #. https://docs.tutor.overhang.io/whatnext.html#importing-a-demo-course

   #. Log into the LMS with your admin user and enroll / proceed through the demo course

#. OR If you are adding Aspects to an existing LMS that already has data

   #. Sink course data from the LMS to clickhouse (see https://github.com/openedx/openedx-event-sink-clickhouse for more information)::

       tutor local do dump-courses-to-clickhouse --options "--force"


   #. Sink Historical event data to ClickHouse::

       tutor [dev|local] do transform_tracking_logs \
         --source_provider LOCAL --source_config '{"key": "/openedx/data", "container":
            "logs", "prefix": "tracking.log"}' \
         --transformer_type xapi

       # Note that this will work only for default tutor installation. If you store your tracking logs any other way, you need to change the source_config option accordingly.
       # See https://event-routing-backends.readthedocs.io/en/latest/howto/how_to_bulk_transform.html#sources-and-destinations for details on how to change the source_config option.


You should now have data to look at in Superset! Log in to https://superset.local.overhang.io/ with your admin account and you should see charts with your data.

Superset Assets
---------------

Aspects maintains the Superset assets in this repository, specifically the dashboards,
charts, datasets, and databases. That means that any updates made here will be reflected
on your Superset instance when you update your deployment.

But it also means that any local changes you make to these assets will be overwritten
when you update your deployment. To prevent your local changes from being overwritten,
please create new assets and make your changes there instead. You can copy an existing
asset by editing the asset in Superset and selecting "Save As" to save it to a new name.


Sharing Charts and Dashboards
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To share your charts with others in the community, use Superset's "Export" button to
save a zip file of your charts and related datasets.

.. warning::
    The exported datasets will contain hard-coded references to your particular
    databases, including your database hostname, port, and username, in some cases
    it may also contain database passwords. It is vital that you review the
    database and dataset files before sharing them.

To import charts or dashboards shared by someone in the community:

#. Expand the zip file and look for any files added under ``databases``.
   Update the ``sqlalchemy_uri`` to match your database's connection details.
#. Compress the files back into a ``.zip`` file.
#. On the Charts or Dashboards page, use the "Import" button to upload your ``.zip`` file.


Contributing Charts and Dashboards to Aspects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Superset assets provided by Aspects can be found in the templated
`tutoraspects/templates/aspects/build/aspects-superset/openedx-assets/assets/` directory. For the most part,
these files are what Superset exports, but with some crucial differences
which make these assets usable across all Tutor deployments.

To contribute assets to Aspects:

#. Fork this repository and have a locally running Tutor set up with this plugin
   installed.
#. Export the assets you want to contribute as described in `Sharing Charts and Dashboards`
#. Run the command:
   `tutor aspects import_superset_zip ~/Downloads/your_file.zip`
#. This command will copy the files from your zip to the assets directory and
   attempt to warn you if there are hard coded connection settings where it expects
   template variables. These are usually in database and dataset assets, and those are
   often assets that already exist. The warnings look like:

   `WARN: fact_enrollments.yaml has schema set to reporting instead of a setting.`
#. Check the diff of files and update any database connection strings or table names
   to use Tutor configuration template variables instead of hard-coded strings, e.g.
   replace ``clickhouse`` with ``{{CLICKHOUSE_HOST}}``. Passwords can be left as
   ``{{CLICKHOUSE_PASSWORD}}``, though be aware that if you are adding new
   databases, you'll need to update ``SUPERSET_DB_PASSWORDS`` in the init scripts.
   Here is the default connection string for reference::

   ``clickhousedb+connect://{{CLICKHOUSE_REPORT_URL}}``
#. You will likely also run into issues where our SQL templates have been expanded into
   their actual SQL. If you haven't changed the SQL of these queries (stored in
   `tutoraspects/templates/openedx-assets/queries` you can just revert that change back
   to their `include` values such as:
   `sql: "{% include 'openedx-assets/queries/fact_enrollments_by_day.sql' %}"`
#. The script will also warn about missing `_roles` in dashboards. Superset does not export
   these, so you will need to manually add this key with the roles that are necessary to
   view the dashboard. See the existing dashboards for how this is done.
#. Re-build your ``aspects-superset`` image with `tutor images build aspects-superset --no-cache`
#. Run the command `tutor aspects check_superset_assets` to confirm there are no
   duplicate assets, which can happen when you rename an asset, and will cause import
   to fail. The command will automatically delete the older file if it finds a duplicate.
#. Check that everything imports correctly by running `tutor local do init -l aspects`
   and confirming there are no errors.
#. Double check that your database password did not get exported before committing!
#. Commit and submit a PR with screenshots of your new chart or dashboards, along with an
   explanation of what data question they answer.


Virtual datasets in Superset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Superset supports creating virtual datasets, which are datasets defined using a SQL query instead of mapping directly to an underlying database object. Aspects leverages virtual datasets, along with `SQL templating <https://superset.apache.org/docs/installation/sql-templating/>`_, to make better use of table indexes.

To make it easier for developers to manage virtual datasets, there is an extra step that can be done on the output of ``tutor aspects serialize``. The ``sql`` section of the dataset yaml can be moved to its own file in the `queries`_ directory and included in the yaml like so:

.. code-block:: yaml

   sql: "{% include 'openedx-assets/queries/query.sql' %}"


However, please keep in mind that the assets declaration is itself a jinja template. That means that any jinja used in the dataset definition should be escaped. There are examples of how to handle this in the existing queries, such as `dim_courses.sql`_.

.. _queries: tutoraspects/templates/openedx-assets/queries/

.. _dim_courses.sql: tutoraspects/templates/openedx-assets/queries/dim_courses.sql

License
-------

This software is licensed under the terms of the AGPLv3.
