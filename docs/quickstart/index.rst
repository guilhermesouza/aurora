Quickstart
==========

To be able to run Aurora you will need:

* Python 2.6 or 2.7
* UNIX-based operating system
* PostgreSQL (Aurora uses SQLAlchemy which allows to use other databases, but development is going on with PostgreSQL)

Setting up an Environment
-------------------------

You need to start by creating a new ``virtualenv``. If you don't have this Python package you can install it with::

    easy_install -UZ virtualenv
    # or 
    pip install virtualenv

After installation create a virtualenv somewhere::

    virtualenv aurora

And activate it::

    source aurora/bin/activate

Installation
------------

Now you can install aurora::

    easy_install -UZ aurora
    # or
    pip install aurora
    # or from git
    pip install git+https://github.com/ak3n/aurora.git#egg=aurora

Configuration
-------------

Aurora uses default config object and you can override it with commands::

    # 1. Will create config at ``~/.aurora/settings.py`` by default.
    aurora init_config

    # 2. Specified config.
    aurora runserver -c /tmp/settings.py # for example

You must change ``SECRET_KEY`` and it would be better for you to use PostgreSQL.

Then you need to initialize you database::

    aurora init_db


Running migrations
------------------

If you are using PostgreSQL and want to migrate::

    aurora migrate upgrade head


Starting an application
--------------------

Aurora dev server can be started with command::

    aurora runserver
