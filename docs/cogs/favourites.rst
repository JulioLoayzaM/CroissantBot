Favourites
==========

The Favourites cog allows the users to have *one* playlist without using a database like the Playlist cog.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_JSONFAV` variable.

Requirements
------------

-  No package is required.
-  Create a JSON file in ``rsc/`` to store the playlists and set the :envvar:`MUSIC_FAV_LIST` variable in ``.env``.
   By default, the name is ``favourites_songs.json``.

How it works
------------

As the requirements show, the setup is minimal.
The cog stores the playlists in a JSON file, using the following template:

   .. code-block:: json

      {
         "discord_user_id_1": [
            {
               "title": "song_name_1",
               "url": "song_url_1",
               "thumbnail": "thumbnail_url_1"
            },
            {
               "title": "song_name_2",
               "url": "song_url_2",
               "thumbnail": "thumbnail_url_2"
            }
         ]
      }

This cog is compatible with the Music cog:

   -  The ``now`` command allows to save the currently playing song to the user's playlist.

   -  The ``play`` commands allows to play a song directly from the user's playlist.

.. seealso::
   The :doc:`Playlist <playlist>` cog uses a PostgreSQL database to store as many playlists per user as needed.