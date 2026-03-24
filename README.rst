=============================
The Aspects Plugin for Tutor
=============================

Aspects Learner Analytics integrates several open-source tools to add powerful analytics and reporting capabilities to the Open edX platform. This plugin enables seamless installation, configuration, and deployment of these tools via `Tutor <https://docs.tutor.overhang.io>`_. The tools integrated by Aspects are:

- `ClickHouse <https://clickhouse.com>`_: A fast and scalable analytics database.
- `Apache Superset <https://superset.apache.org>`_: A data visualization and exploration platform.
- `OpenFUN Ralph <https://openfun.github.io/ralph/>`_: A Learning Record Store that validates and stores xAPI statements in ClickHouse.
- `Vector <https://vector.dev>`_: A tool for forwarding logs and xAPI data to ClickHouse.
- `Event-Routing-Backends <https://event-routing-backends.readthedocs.io/en/latest/>`_: An Open edX plugin that transforms tracking logs into xAPI and forwards them to Learning Record Stores in near real-time.
- `dbt <https://www.getdbt.com>`_: A SQL-based data pipeline builder, utilizing the `aspects-dbt <https://github.com/openedx/aspects-dbt>`_ project.

For more information, refer to the `Aspects architecture documentation <https://docs.openedx.org/projects/openedx-aspects/en/latest/technical_documentation/concepts/aspects_overview.html>`_.

Key Features
============

- Streamlined deployment of analytics and reporting tools.
- Integration with Open edX for real-time and historical data analytics.
- Extensible architecture supporting customization.
- Open edX Teak or higher: `In-context metrics in Studio`.


Compatibility
=============

Current versions of the plugin are compatible with Tutor 19.0.0 and later and support Open edX releases from Sumac onward. Older releases can support Open edX versions as far back as Nutmeg. Details are available in the `Aspects Documentation <https://docs.openedx.org/projects/openedx-aspects/en/latest/technical_documentation/how-tos/upgrade.html>`_.


Breaking Changes
================

As of Aspects V4 the default data pipeline has changed from Ralph to Vector. This change improves performance and simplifies the architecture by eliminating the need to scale multiple Ralph containers and Celery workers for high-throughput scenarios.

Key changes:

- Vector is now the default for xAPI event ingestion
- The ``ASPECTS_VECTOR_RAW_XAPI_TABLE`` setting has been replaced with ``ASPECTS_RAW_XAPI_TABLE``
- The default database has changed from ``xapi`` (Ralph) to ``openedx`` (Vector)

To keep using Ralph as your data pipeline:

.. code-block:: bash

   tutor config save --set ASPECTS_XAPI_SOURCE=ralph
   tutor config save --set RUN_RALPH=True
   tutor config save --set RUN_VECTOR=False

This will configure Aspects to use Ralph with the ``xapi`` database, preserving your existing data.

If you have customized ``ASPECTS_VECTOR_RAW_XAPI_TABLE`` in your configuration, update it to use ``ASPECTS_RAW_XAPI_TABLE`` instead.

For new installations or users switching to Vector, your data will be stored in the ``openedx`` database. You can migrate existing data from the ``xapi`` database to ``openedx`` if needed.


Installation
============

Aspects is implemented as a Tutor plugin. For now, the easiest installation method is via Tutor. Follow these steps for a ``tutor local`` installation:

#. **Install Tutor**:
   Follow the instructions at `Tutor Installation Guide <https://docs.tutor.overhang.io/install.html#install>`_.

#. **Create an Admin User**:
   Refer to the `Tutor Setup Guide <https://docs.tutor.overhang.io/whatnext.html#logging-in-as-administrator>`_.

#. **Install and Enable the Plugin**:

   .. code-block:: bash

      pip install tutor-contrib-aspects
      tutor plugins enable aspects
      tutor config save

#. **Turn on In-Context Metrics (Optional)**:
   If using Open edX Teak or higher, `in-context metrics` can be enabled in Studio. See `frontend-plugin-aspects` for more information.

#. **Rebuild Docker Images**:

   .. code-block:: bash

      tutor images build openedx --no-cache
      tutor images build mfe --no-cache  # Only necessary if using in-context metrics
      tutor images build aspects aspects-superset

#. **Initialize the Environment**:

   .. code-block:: bash

      tutor local do init

Data Population Options
------------------------

To visualize data:

- Generate test data:

  .. code-block:: bash

     tutor local do load-xapi-test-data

- Import a demo course and create real data:

  Follow `these steps <https://docs.tutor.overhang.io/whatnext.html#importing-a-demo-course>`_.

- Interact with the course to generate data:

   Complete a few activities within the course (e.g., enroll, take quizzes, watch videos) to generate real data. This will provide a more realistic dataset for analytics.



xAPI S3 Sink Configuration
-------------------------

The S3 sink serves as a backup and safeguard for xAPI events. If ClickHouse is unavailable or encounters errors during event ingestion, events are stored in S3 as a safeguard. This ensures data durability and allows you to recover missed events later using the ``xapi-backfill`` command.

To enable this backup mechanism, configure the following settings:

.. code-block:: yaml

   ASPECTS_XAPI_S3_ACCESS_KEY=openedx
   ASPECTS_XAPI_S3_BUCKET=xapi-events
   ASPECTS_XAPI_S3_ENDPOINT=http://minio:9000
   ASPECTS_XAPI_S3_REGION=us-east-1
   ASPECTS_XAPI_S3_SECRET_KEY=...

Vector S3 sink options:

.. code-block:: bash

   ASPECTS_XAPI_S3_SINK_MAX_EVENTS=10000
   ASPECTS_XAPI_S3_SINK_TIMEOUT_SECS=600

.. note::

   - ``ASPECTS_XAPI_S3_SINK_MAX_EVENTS`` controls how many events are batched before writing to S3
   - ``ASPECTS_XAPI_S3_SINK_TIMEOUT_SECS`` controls how long to wait before flushing a batch
   - Setting ``ASPECTS_XAPI_S3_SINK_TIMEOUT_SECS`` too low can create many small files in S3


xAPI S3 Backfill
----------------

If you have xAPI events stored in S3 (configured via ``ASPECTS_XAPI_S3_BUCKET``), you can backfill them into ClickHouse using the ``xapi-backfill`` command. This is useful for:

- Restoring data from a backup
- Importing data from another environment
- Re-processing historical events

Basic usage:

.. code-block:: bash

   tutor local do xapi-backfill

By default, this imports all events. You can filter by date using year, month, day, and hour options:

.. code-block:: bash

   tutor local do xapi-backfill --year 2026 --month 3
   tutor local do xapi-backfill --year 2026 --month 03 --day 19
   tutor local do xapi-backfill --year 2026 --month 03 --day 19 --hour 14

For flexible path matching, use the ``--path`` option to specify a custom S3 path:

.. code-block:: bash

   tutor local do xapi-backfill --path xapi/2026/03/19/14/*.log.zst

.. note::

   - Date options accept both single and double-digit values (``03`` and ``3`` are equivalent)
   - Hour should be in 24-hour format
   - The ``--path`` option is exclusive with date options

After backfilling, you can run deduplication to remove duplicate events:

.. code-block:: bash

   tutor local do xapi-backfill --deduplicate

Or run deduplication separately:

.. code-block:: bash

   tutor local do xapi-deduplicate

.. warning::

   Deduplication uses ``OPTIMIZE TABLE FINAL`` which can be resource-intensive on large tables. Run during low-traffic periods if you have a large dataset.


- Sync data from an existing Tutor installation with default settings:

  .. code-block:: bash

     tutor local do dump-data-to-clickhouse --options "--object course_overviews"
     tutor local do transform-tracking-logs --source_provider LOCAL --source_config '{"key": "/openedx/data", "container": "logs", "prefix": "tracking.log"}' --transformer_type xapi

Superset and Autoscaling
=========================

Superset Assets
---------------

Aspects maintains its Superset assets (dashboards, charts, datasets) in the repository. Local changes to these assets will be overwritten during updates unless saved as new assets.

To rebuild and re-import assets:

.. code-block:: bash

   tutor images build aspects-superset --no-cache
   tutor local do import-assets

Autoscaling
-----------

Aspects supports Kubernetes autoscaling configurations for Ralph, Superset, and Superset Worker via the `Pod Autoscaling plugin <https://github.com/eduNEXT/tutor-contrib-pod-autoscaling>`_. Modify autoscaling settings as needed.

Contributing Charts and Dashboards
===================================

To contribute Superset assets:

#. Fork this repository and set up a local Tutor instance with Aspects installed.
#. You should work on the non-localized versions of the Superset dashboards. Export the new or updated dashboard(s) using Superset’s “Export” feature. It is best to export the entire dashboard instead of just charts or datasets to ensure that all of the correct changes are captured.
#. Use the command:

   .. code-block:: bash

      tutor aspects import_superset_zip ~/Downloads/your_file.zip

#. Update database connection strings to use template variables.
#. Validate and rebuild:

   .. code-block:: bash

      tutor images build aspects-superset --no-cache
      tutor aspects check_superset_assets
      tutor local do import-assets

#. Submit a pull request with screenshots and details of your contributions.

Release Workflow
================

Releases are handled by repository maintainers via GitHub Actions:

- Trigger the **Bump version and changelog** action to update the version and changelog.
- Merge the PR to initiate the **release** and **build-image** workflows.

Ensure the updated version appears on `PyPI <https://pypi.org>`_ and DockerHub.

Additional Resources
=====================

- `Tutor Documentation <https://docs.tutor.overhang.io>`_
- `Aspects Beta Progress <https://openedx.atlassian.net/wiki/spaces/COMM/pages/3861512203/Aspects+Beta>`_
- `Superset Documentation <https://superset.apache.org/docs>`_
- `DBT Documentation <https://www.getdbt.com/docs/>`_
- `Event Routing Backends Documentation <https://event-routing-backends.readthedocs.io/en/latest/>`_
- `Tracking Logs Documentation <https://vector.dev/docs/>`_


.. _frontend-plugin-aspects: https://github.com/openedx/frontend-plugin-aspects
.. _in-context metrics: https://docs.openedx.org/projects/openedx-aspects/en/latest/technical_documentation/how-tos/production_configuration.html#in-context-metrics
.. _in-context metrics in Studio:  https://docs.openedx.org/projects/openedx-aspects/en/latest/reference/in_context_dashboards.html