Youtube
=======

This Cog enables the bot's YouTube livestream-checking capabilities. It
uses :py:mod:`streamlink` to get the stream's URL and :py:mod:`yt_dlp` to get the
stream's title and thumbnail.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_YT` variable.

Requirements
------------

Packages
^^^^^^^^

-  The :py:mod:`streamlink` package:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U streamlink

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U streamlink

.. versionadded:: 1.1.0

-  The :py:mod:`yt_dlp` package:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U yt-dlp

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U yt-dlp

   .. note::
      For backwards compatibility with the pre-v1.1.0 Music cog, the
      :py:mod:`youtube-dl` package can be used. However its use in this bot is
      deprecated and installing :py:mod:`yt-dlp` is recommended.

env variables
^^^^^^^^^^^^^

-  :envvar:`YT_FILE` represents the path to a JSON file which contains the IDs of
   the Discord users to notify, and the info of the streamers to check.

-  This cog implicitly uses the :envvar:`TW_FREQUENCY` variable from the Twitch cog.
   It indicates how often the bot checks the streams, in minutes.
   If need be, just create :envvar:`YT_FREQUENCY` in ``.env`` and make the appropriate changes in :py:mod:`bot.py`.

Format used by YT_FILE
----------------------

The format to use for :envvar:`YT_FILE` is as follows:

.. code-block:: json

   {
      "discord_user_ID_1": {
         "youtube_channel_1": {
            "nickname": "streamers_nickname_1",
            "url": "channel_url_1"
         },
         "youtube_channel_2": {
            "nickname": "streamers_nickname_2",
            "url": "channel_url_2"
         }
      },
      "discord_user_ID_2": {
         "youtube_channel_1": {
            "nickname": "streamers_nickname_1",
            "url": "channel_url_1"
         },
         "youtube_channel_3": {
            "nickname": "streamers_nickname_3",
            "url": "channel_url_3"
         }
      }
   }

.. note::
   The ``youtube_channel`` and ``nickname`` keys are arbitrary.
   ``youtube_channel`` is used to make it easier to identify the
   channel in the logs, while ``nickname`` is used to have an
   identifiable name in the message (since we can't get that info
   through the API). They can have the same value.

Fill it with the corresponding information and set :envvar:`YT_FILE` in
``.env``. The Discord user's ID can be found by right-clicking the
user's name.