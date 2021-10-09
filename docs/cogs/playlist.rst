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

This cog uses PostgreSQL, a "powerful, open source object-relational database system".
To install it, check its `downloads page <https://www.postgresql.org/download/>`_.
If you haven't installed PostgreSQL before, I recommend using version 13 since it's the one I used to develop this cog.

If you have question regarding its usage, their "world-renowned" documentation is the place to go.

Music cog
---------

As the Favourites cog, this cog has two commands that use the Music cog:

-  ``now`` adds the currently playing song to the default 'favourites' list or one specified by the user.

-  ``play`` queues a playlist or a specific song from a playlist.

It also uses the :py:class:`YTDLSource` class that comes in the Music cog to generate the :py:class:`Song` to save with ``add``.

yt-dlp
------

This package is used to verify the URL passed to this cog is a valid Youtube URL.