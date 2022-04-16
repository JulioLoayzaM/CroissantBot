Twitch
======

This Cog enables the bot's Twitch livestream-checking capabilities.

It uses Twitch's API to get the information needed.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_TW` variable.

Packages
--------

No Twitch package is needed.
It uses :py:mod:`requests`, which should be already installed.
If it's not, the package can be installed with ``pip`` or ``pipenv``.

env variables
-------------

.. csv-table::
   :file: twitch-vars.csv
   :header-rows: 1
   :delim: ,

Using Twitch's API
------------------

To use the API, we need the **Client ID** and **Secret**.
To get them, follow Step 1 of this
`getting started guide <https://dev.twitch.tv/docs/api/#step-1-register-an-application>`__.
Fill :envvar:`TW_CLIENT_ID` and :envvar:`TW_CLIENT_SECRET` with these values.

Then, we need an **Access Token**.
Normally the bot takes care of this: the tokens expire so the bot regularly checks its validity.
If the token is invalid, or it can't be found in ``.env``, the bot automatically gets a new token
and saves it in :envvar:`TW_TOKEN`.

If for some reason this fails, see :ref:`cogs/twitch:manually getting an access token`.

-  Finally, set :envvar:`TW_FREQUENCY`. This variable indicates how often the bot will check Twitch, in minutes.
   It should be a string, casting it to ``int`` is done in :py:mod:`bot.py`.

How to use this cog
-------------------

In order to indicate which streamers the bot should check, and which users it should notify,
it uses the :envvar:`TW_FILE` JSON file.

It is a dictionary where the keys are the IDs of the Discord users to notify,
and the values are a list of the streamers to check for each user.

A Discord user's ID can be found by right-clicking the user's name.
You can either use the URL of the streamer's channel or its ``user_login``,
which is the last portion of the channel's URL.

For example:

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

Manually getting an access token
--------------------------------

.. attention::
   You can use the following methods to get an access token, but keep in mind that they will still expire,
   meaning that you will have to renew it every 60 days.
   If the automatic way is not working, I suggest opening an issue
   `in the repo <https://github.com/JulioLoayzaM/CroissantBot/issues>`_.

To manually get an access token, you can use:

1. The Twitch CLI, as described in
   `Step 2 <https://dev.twitch.tv/docs/api/#step-2-authentication-using-the-twitch-cli>`__
   of the Twitch API guide.

2. A simple script, based on `this Stack Overflow answer <https://stackoverflow.com/a/66536359>`__:

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
