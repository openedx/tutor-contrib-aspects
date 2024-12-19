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




Compatibility
=============

The plugin is compatible with Tutor 15.0.0 and later and supports Open edX releases from Nutmeg onward.

Installation
============

Aspects is implemented as a Tutor plugin. For now, the easiest installation method is via Tutor. Follow these steps for a ``tutor local`` installation:

1. **Install Tutor**:
   Follow the instructions at `Tutor Installation Guide <https://docs.tutor.overhang.io/install.html#install>`_.

2. **Create an Admin User**:
   Refer to the `Tutor Setup Guide <https://docs.tutor.overhang.io/whatnext.html#logging-in-as-administrator>`_.

3. **Install and Enable the Plugin**:

   .. code-block:: bash

      pip install tutor-contrib-aspects
      tutor plugins enable aspects
      tutor config save

4. **Rebuild Docker Images**:

   .. code-block:: bash

      tutor images build openedx --no-cache
      tutor images build aspects aspects-superset

5. **Initialize the Environment**:

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

1. Fork this repository and set up a local Tutor instance with Aspects installed.
2. You should work on the non-localized versions of the Superset dashboards. Export the new or updated dashboard(s) using Superset’s “Export” feature. It is best to export the entire dashboard instead of just charts or datasets to ensure that all of the correct changes are captured.
3. Use the command:

   .. code-block:: bash

      tutor aspects import_superset_zip ~/Downloads/your_file.zip

4. Update database connection strings to use template variables.
5. Validate and rebuild:

   .. code-block:: bash

      tutor images build aspects-superset --no-cache
      tutor aspects check_superset_assets
      tutor local do import-assets

6. Submit a pull request with screenshots and details of your contributions.

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
