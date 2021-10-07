Twitch
======

This Cog enables the bot's Twitch livestream-checking capabilities. It
uses Twitch's API to get the information needed.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_TW` variable.

Requirements
------------

Packages
^^^^^^^^

-  No Twitch package is needed. It uses :py:mod:`requests`, which should be
   already installed. If it's not, the package can be installed with
   :py:mod:`pip`:

   .. code-block:: bash

      pip install -U requests

env variables
^^^^^^^^^^^^^

-  To use the API, we need the **Client ID** and **Secret**. To
   get them, follow Step 1 of this `getting started
   guide <https://dev.twitch.tv/docs/api/#step-1-register-an-application>`__.
   Fill :envvar:`TW_CLIENT_ID` and :envvar:`TW_CLIENT_SECRET` with these values.

-  Then, we need an **Access Token**. Normally the bot takes care of it, you just need to uncomment
   :envvar:`TW_TOKEN` and leave it blank. When the bot checks the token validity at startup, it will
   notice the token is empty and will automatically try to get a valid token and save it in :envvar:`TW_TOKEN`.
   If for some reason this fails, see :ref:`cogs/twitch:manually getting an access token`.

-  :envvar:`TW_FILE` represents the path to a JSON file that stores
   the IDs of the Discord users to notify, and the Twitch channels to check for each one.
   The name of the file is ``twitch_ids.json`` by default.
   You can use the example file provided, but **please change its name** since leaving it as is
   may result in overwritting when updating the bot with :program:`git pull`.

-  Finally, set :envvar:`TW_FREQUENCY`. This variable indicates how often the bot will check Twitch, in minutes.
   It should be a string, casting it to ``int`` is done in :py:mod:`bot.py`.

Format used by TW_FILE
----------------------

The format to use for :envvar:`TW_FILE` is as follows:

      .. code-block:: json

         {
            "discord_user_ID_1":
               [
                  "twitch_channel_1",
                  "twitch_channel_2"
               ],
            "discord_user_ID_2": 
               [
                  "twitch_channel_1",
                  "twitch_user_login_3"
               ]
         }

Fill it with the corresponding information and set :envvar:`TW_FILE` in
``.env``. A Discord user's ID can be found by right-clicking the user's
name. You can either use the URL of the streamer's channel or its
``user_login``, which is the last portion of said URL.

Manually getting an access token
--------------------------------

.. attention::
   API tokens expire. When this happens, the bot tries to get a new one automatically.
   If the automatic way failed, you may have to get a new token each 60 days, or the cog won't work.
   In this case, I suggest opening an issue `in the repo <https://github.com/JulioLoayzaM/CroissantBot/issues>`_.

If the automatic way of getting an access token fails, there are two manual ways of getting it:

1. The Twitch CLI is one option.
   `Step 2 <https://dev.twitch.tv/docs/api/#step-2-authentication-using-the-twitch-cli>`__
   of the aforementioned guide explains how to use it.

2. A simple script (based on `this Stack Overflow answer <https://stackoverflow.com/a/66536359>`__)
   can be used instead of downloading the CLI:

   .. code:: python

      import requests

      # Fill these variables with the credentials obtained
      # on the previous step.
      client_id = ''
      client_secret = ''

      body = {
         'client_id': client_id,
         'client_secret': client_secret,
         'grant_type': "client_credentials"
      }
      r = requests.post('https://id.twitch.tv/oauth2/token', body)

      keys = r.json()

      print(keys)

   A sample result of the above script:

   .. code:: json

      {
         "access_token": "132456789abcdefgh",
         "expires_in": 3600,
         "token_type": "bearer"
      }

   ``access_token`` is the token you need.
   ``expires_in`` indicates how many seconds the token will remain valid since the request.
