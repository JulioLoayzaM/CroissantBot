Running the bot
===============

A guide on how to create the bot on Discord and add it to a server.

Requirements
------------

* The :py:mod:`discord.py[voice]` package, which can be installed with :py:mod:`pip`:

   .. code-block:: bash

      pip3 install -U discord.py[voice]

*  The :py:mod:`python-dotenv` package, used to get the credentials from the ``.env`` file,
   can be installed with :py:mod:`pip`:

   ::

      pip3 install -U python-dotenv

* The :py:mod:`packaging` package, which may be already included, can be installed with :py:mod:`pip`:

   .. code-block:: bash

      pip3 install -U packaging

*  Create the ``logs`` directory and the four log files needed:
   ``info.log``, ``debug.log``, ``discord.log`` and ``streamlink.log``.
   Then uncomment the ``.env`` variables.
   The bot will use these files as a base and rotate the logs at midnight.
   This means a day's worth of logs will be saved on a separate file and the current file will be reset.
   By default, it keeps up to 7 days of logs as indicated by :envvar:`LOG_COUNT`.

.. note::
   ``streamlink.log`` is only needed when using the :doc:`youtube` cog, but it's better to create it now than wonder why the bot can't find the file.


Creating the bot
----------------

To create the bot on Discord's side of things and get the bot's token, I recommend following `this guide <https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal>`_. Here's a quick rundown of the steps to follow:

- If needed, create a Discord account and verify your email.
- Login to the `developer portal <https://discord.com/developers/applications>`_.
- Create a new application.
- In the Bot section (on the left), create a bot. You can change the default name.
- Grab the token.
- Scroll down and enable the ``server members intent`` under Privileged Gateway intents.


Adding it to a server
---------------------

To add the bot to a server (a guild in the API's terminology) see `this part <https://realpython.com/how-to-make-a-discord-bot-python/#adding-a-bot-to-a-guild>`_ of the previous guide. Essentially:

- In the `developer portal <https://discord.com/developers/applications>`_, go to the OAuth2 tab.

- In the OAuth2 URL Generator, select *bot* in Scopes.

- As for permissions, there are two options:

  -  For a private server, Administrator is the easier choice.
  -  For a bigger or more public server, it's better to select only the permissions needed for the bot to run correctly.

For now, the permissions I'm using with the bot are:

.. list-table::
   :header-rows: 1

   * - Permissions
   * - View channels
   * - Send messages
   * - Embed links
   * - Attach files
   * - Add reactions [not used yet]
   * - Manage messages
   * - Read message history
   * - Use Application Commands
   * - Connect
   * - Speak
   * - Use voice activity
