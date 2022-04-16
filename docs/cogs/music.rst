Music
=====

This Cog contains the bot's music-playing commands.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_MUSIC` variable.

Packages
--------

-  :py:mod:`yt-dlp` is used to download music from Youtube.

-  It uses :program:`FFmpeg` to extract the audio.
   Install instructions can be found at `ffmpeg.org <https://www.ffmpeg.org/>`__.

.. versionadded:: 1.1.0
   The :py:mod:`yt-dlp` package.

.. deprecated:: 1.1.0
   The use of the :py:mod:`youtube-dl` package in this bot is deprecated.
   Backwards compatibility is maintained but installing :py:mod:`yt-dlp` is recommended.

env variables
-------------

.. csv-table::
   :file: music-vars.csv
   :header-rows: 1
   :delim: ,

.. versionadded:: 3.0.0
   ``config.py`` creates the :envvar:`MUSIC_DIR` directory.

How it works
------------

Videos are downloaded with :py:mod:`yt-dlp` and the audio is extracted with :program:`FFmpeg`.
This means that the songs take space in your drive and may take some time before being playable,
depending on your network speed.

To avoid downloading really long songs and taking ages to begin playback,
the :envvar:`MAX_DURATION` variable was added to limit the length of the songs.

Also note that the downloads folder is not cleaned at all:
the songs have to be deleted manually, but if the bot has to play a song it already downloaded,
it will be able to do so faster than when the song was first requested.
