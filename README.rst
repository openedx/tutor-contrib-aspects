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


License
-------

This software is licensed under the terms of the AGPLv3.
