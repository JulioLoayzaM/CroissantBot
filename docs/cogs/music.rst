Music
=====

This Cog contains the bot's music-playing commands.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_MUSIC` variable.

Requirements
------------

- The :py:mod:`yt-dlp` package, which can be installed with :py:mod:`pip`:

   .. code-block:: bash

      pip3 install -U yt-dlp

-  :program:`FFmpeg` is used by :py:mod:`yt-dlp` to extract the audio. Install
   instructions can be found at `ffmpeg.org <https://www.ffmpeg.org/>`__.

-  The :envvar:`MAX_DURATION` variable from ``.env`` indicates the maximum
   length in seconds a video can have in order to be downloaded. The
   default is 600 seconds or 10 minutes.

-  :envvar:`MUSIC_DIR` indicates where to download the music. Create the
   directory and set the variable accordingly.

.. versionadded:: 1.1.0
   The :py:mod:`yt-dlp` package.

.. deprecated:: 1.1.0
   The use of the :py:mod:`youtube-dl` package in this bot is deprecated.
   Backwards compatibility is maintained but installing :py:mod:`yt-dlp` is recommended.

How it works
------------

The bot uses :py:mod:`yt-dlp` to download the video and extracts the audio
using :program:`FFmpeg`. This means the songs take drive space. It also means
that playing a song for the first time may take a bit while the download
finishes. But if this cache isn't cleared, the next time the same song
is requested there should be no delay in playing it.
