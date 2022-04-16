Youtube
=======

This Cog enables the bot's YouTube livestream-checking capabilities.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_YT` variable.

Packages
--------

It uses :py:mod:`streamlink` to get the stream's URL and
:py:mod:`yt_dlp` to get the stream's title and thumbnail.

.. note::
   For backwards compatibility with the pre-v1.1.0 Music cog,
   the :py:mod:`youtube-dl` package can be used.
   However its use in this bot is deprecated and installing :py:mod:`yt-dlp` is recommended.

env variables
-------------

:envvar:`YT_FILE` is the path to the JSON file which contains the IDs of
the Discord users to notify and the info of the streamers to check.

.. note::
   This cog implicitly uses the :envvar:`TW_FREQUENCY` variable from the Twitch cog
   to know how ofter the bot should check for streams.

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
   ``youtube_channel`` is used to make it easier to identify the channel in the logs,
   while ``nickname`` is used to have an identifiable name in the message
   (since we can't get that info through the API).
   They can have the same value.
