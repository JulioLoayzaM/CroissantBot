ext modules
===========

These modules provide classes used by the cogs.
They are primarily built around the rest of CroissantBot's code,
but they could be useful when creating a new cog.

For music
---------

-  The :py:mod:`song` module provides the :py:class:`song.Song` class,
   which represents a single song and stores its info.

-  The :py:mod:`songqueue` module provides the :py:class:`songqueue.SongQueue` class,
   which implements a queue that deals with :py:class:`song.Song` instances.

For PostgreSQL databases
------------------------

The :py:mod:`db` module provides the base :py:class:`db.DatabaseConnection` class.
It can connect and disconnect from a database, and check whether it is currently connected.

The :py:mod:`music_db` module provides the :py:class:`music_db.MusicDatabaseConnection` class,
which can manage the music database used by the :ref:`Playlist cog <cogs/playlist:playlist>`.