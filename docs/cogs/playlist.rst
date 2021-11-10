Playlist
========

.. versionadded:: 2.0.0

This cog adds the possibility to have as many playlists per user as you want.
It is compatible with the Music cog; see below for commands.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_PLAYLISTS` variable.

Requirements
------------

Packages
^^^^^^^^

-  The :py:mod:`asyncpg` package:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U asyncpg

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U asyncpg

-  The :py:mod:`yt-dlp` package:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U yt-dlp

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U yt-dlp

env variables
^^^^^^^^^^^^^

The :envvar:`DB_MUSIC` variables.
These are used by the :py:class:`MusicDatabaseConnection` class to connect to the database containing the playlists.

Creating the database
---------------------

This cog uses `PostgreSQL <https://www.postgresql.org/>`_, a "powerful, open source object-relational database system".
Its documentation is quite detailed, don't hesitate to check it out when in doubt.

A quick guide on setting up PostgreSQL can be found at `<https://pimylifeup.com/raspberry-pi-postgresql/>`_.

For this cog, the steps to follow are:

1. Install PostgreSQL: check its `downloads page <https://www.postgresql.org/download/>`_.
   If you haven't installed PostgreSQL before, I recommend using version 13 since it's the one I used to develop this cog.

2. Switch to user ``postgres`` with:

   .. code-block:: bash

      sudo su postgres

3. Create a new role. You can use any username you want. Use the command:

   .. code-block:: bash

      createuser <username> -P -D -R -S

   This creates a role named username. It requires creating a password (``-P``).
   The role cannot create databases (``-D``), roles (``-R``) and won't be a superuser (``-S``).

4. Launch the CLI with the ``psql`` command (while still connected as user ``postgres``).

5. Create the database. You can use any name (except ``songs``, ``playlists`` or ``songs_in_playlists`` to avoid any confusion).
   You can name it ``music`` for example. Use the command:

   .. code-block:: psql

      CREATE DATABASE <name> OWNER <username>;

   Where ``username`` is the name of the user created in step 3.

6. You can now exit the CLI with ``\q`` and return to your usual user with ``exit``.

7. Set the ``.env`` variables starting with :envvar:`DB_MUSIC`:

   -  :envvar:`HOST` should be ``localhost``.
   -  :envvar:`USER` is the name of the user you created in step 3.
   -  :envvar:`PASSWORD` is that user's password.
   -  :envvar:`DATABASE` is the name of the database (``music`` in the example).
   -  :envvar:`PORT` is the port used to connect to the database. By default, its 5432.

8. Once the variables are set, use the ``db_setup.py`` script to create the tables needed by the cog:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 db_setup.py

.. tab:: Windows

   .. code-block:: batch

      py db_setup.py

9. That should be it. :)

.. important::

   If you turn off or reset the computer in which the bot is running, you may need to restart the database server.
   Use the command ``sudo service postgresql start`` to do so.

Music cog
---------

As the Favourites cog, this cog has two commands that use the Music cog:

-  ``now`` adds the currently playing song to the default 'favourites' list or one specified by the user.

-  ``play`` queues a playlist or a specific song from a playlist.

It also uses the :py:class:`YTDLSource` class that comes in the Music cog to generate the :py:class:`Song` to save with ``add``.
This **does not** require enabling the Music cog in order to work.

yt-dlp
------

This package is used to verify the URL passed to this cog is a valid Youtube URL.