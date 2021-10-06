Youtube
=======

This Cog enables the bot's YouTube livestream-checking capabilities. It
uses :py:mod:`streamlink` to get the stream's URL and :py:mod:`yt_dlp` to get the
stream's title and thumbnail.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_YT` variable.

Requirements
------------

-  The :py:mod:`streamlink` package, which can be installed with :py:mod:`pip`:

   .. code-block:: bash

      pip3 install -U streamlink

.. versionadded:: 1.1.0

-  The :py:mod:`yt_dlp` package, which can be installed with :py:mod:`pip`:

   .. code-block:: bash

      pip3 install -U yt-dlp

   .. note::
      For backwards compatibility with the pre-v1.1.0 Music cog, the
      :py:mod:`youtube-dl` package can be used. However its use in this bot is
      deprecated and installing :py:mod:`yt-dlp` is recommended.

-  The :envvar:`YT_FILE` variable in ``.env`` must be set. It represents the
   path to a JSON file which contains the IDs of the Discord users to
   notify and the info of the streamers to check.

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

-  Finally, the Cog implicitly uses :envvar:`TW_FREQUENCY`, which indicates
   how often the bot checks the streams, in minutes. This is used in
   ``bot.py`` and is shared with ``twitch.py``. If need be, just create
   :envvar:`YT_FREQUENCY` in ``.env`` and make the appropriate changes in
   ``bot.py``.
