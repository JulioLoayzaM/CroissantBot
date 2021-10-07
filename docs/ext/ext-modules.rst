ext modules
===========

These modules provide classes used by the cogs.
They are primarily built around the rest of CroissantBot's code, but they
could be useful when creating a new cog.

For music
---------

The :ref:`queue <ext/queue:queue module>` and :ref:`song <ext/song:song module>` modules are provided:

-  The :py:mod:`song` module provides the :py:class:`Song` class, which represents a single song and stores its info.

-  The :py:mod:`queue` module provides the :py:class:`Queue` class, which implements a queue that deals with :py:class:`Song` instances.

For PostgreSQL databases
------------------------

The :ref:`ext/db:db module` is provided. It provides two classes:

-  A base class (:py:class:`DatabaseConnection`) which can connect and disconnect from a database, and check whether it is currently connected.

-  A class (:py:class:`MusicDatabaseConnection`) to manage the music database used by the :ref:`Playlist cog <cogs/playlist:playlist>`.