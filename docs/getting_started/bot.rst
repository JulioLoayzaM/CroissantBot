Running the bot
===============

A guide on how to create and run the bot.

Intro
-----

-  CroissantBot's main file is :py:mod:`bot.py`. This contains the code to run the base bot.
   This includes the ``exit``, ``help``, ``ping``, ``test`` and ``version`` commands.

   .. tip::
      For more commands, see :ref:`cogs/intro-cogs:intro to cogs`.

-  CroissantBot uses a file called ``.env`` to store its settings and credentials.

-  The **bot's default prefix** is ``!``.

Dependencies
------------

This a list of all the packages used by the bot and its cogs.
For the packages needed to run the base bot, see :ref:`getting_started/bot:packages` below.

I've tested the bot with Python 3.6.9 in Ubuntu 18.04 and Python 3.6.1 in Windows 10 using the following packages:

.. csv-table::
   :file: dependencies.csv
   :header-rows: 1
   :delim: ,

.. deprecated:: 1.1.0
   The :py:mod:`youtube-dl` package was used for the Music cog, but since it appears to no longer be maintained,
   using :py:mod:`yt-dlp` is recommended.

.. versionadded:: 2.0.0
   The :py:mod:`asyncpg` package.

.. versionadded:: 2.0.0
   The Playlist cog, which also uses the :py:mod:`yt-dlp` package.

Requirements
------------

Packages
^^^^^^^^

*  The :py:mod:`discord.py[voice]` package:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U discord.py[voice]

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U discord.py[voice]

*  The :py:mod:`python-dotenv` package:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U python-dotenv

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U python-dotenv

*  The :py:mod:`packaging` package may be already included, but can be installed with :py:mod:`pip`:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U packaging

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U packaging

env variables
^^^^^^^^^^^^^

The file provided is actually called ``.env.example`` and not ``.env``.
It contains all the variables the bot may use, alongside some comments on their use.

The base ``.env`` variables to set are:

*  :envvar:`DISCORD_TOKEN`: the bot's token. Check the section :ref:`getting_started/bot:creating the bot` to know how to get it.

*  :envvar:`BOT_PREFIX`: the bot's prefix, which is the character used before a command to invoke the bot.
   It's set to ``!`` by default, but you can change it; just make sure it doesn't interfere with the prefix of other bots you use.

*  The log files:

   *  Create the ``logs`` directory.
   *  Create the four log files needed:
      ``info.log`` (stores INFO-level logs), ``debug.log`` (stores DEBUG-level logs), ``discord.log`` (stores DEBUG-level logs generated by  :py:mod:`discord.py`) and ``streamlink.log`` (stores logs generated by :py:mod:`streamlink`).
   *  Set the corresponding variables to their paths, relative to ``bot.py``, like the ones already written.

*  :envvar:`LOG_COUNT`: the logs files are emptied at midnight and their contents stored in an additional file (named ``something.log.202x-xx-xx``). This variable indicates how many files of each log should be stored at once. By default the bot saves a week's worth of logs.

.. note::
   ``streamlink.log`` is only needed when using the :doc:`./../cogs/youtube` cog, but it's better to create it now than wonder why the bot can't find the file.

Creating the bot
----------------

There are two parts to creating the bot: the code itself (which in this case is already provided) and creating an application
and its corresponding bot in Discord.

Discord's side
^^^^^^^^^^^^^^

To create the bot on Discord's side of things and get the bot's token, I recommend following `this guide <https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal>`_. Here's a quick rundown of the steps to follow:

- If needed, create a Discord account and verify your email.
- Login to `Discord's developer portal <https://discord.com/developers/applications>`_.
- Create a new application.
- In the Bot section (on the left), create a bot. You can change the default name.
- Grab the token.
- Scroll down and enable the ``server members intent`` under Privileged Gateway intents.

Code side
^^^^^^^^^

Keep reading to learn how to actually install the source code and run the bot.

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
      * - Add reactions (not used yet)
      * - Manage messages
      * - Read message history
      * - Use Application Commands
      * - Connect
      * - Speak
      * - Use voice activity

You can set the bot to public, allowing anyone who has the link you generated to invite the bot to their server,
provided they have the necessary permissions (Manage server permission).
Or you can leave the bot as private, which means only you can use the link to add the bot to any server in which you have
the Manage server permission.

Installation and setup
----------------------

Now, time to install the source code and run the bot!

-  If you have a GitHub account, `clone the
   repo <https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository>`__.
-  If not, create one or download the code from the `releases
   page <https://github.com/JulioLoayzaM/CroissantBot/releases>`__ (preferably the latest one, since this guide is written for version 2.0.0).

   .. note::
      Cloning the repo is recommended in order to use Git to easily update the bot.

-  Install Python 3.6+: use your package manager or head over to `the
   download page <https://www.python.org/downloads/>`__.

   -  This should install :py:mod:`pip`, Python's package installer. If unsure,
      read :py:mod:`pip`'s `getting started <https://pip.pypa.io/en/stable/getting-started/>`__ to
      verify and install it if needed.

-  Optional but recommended: create a `virtual
   environment <https://python.land/virtual-environments/virtualenv>`__
   to avoid conflicts with the dependencies.

-  To install all the package dependencies, use:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U -r requirements.txt

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U -r requirements.txt

   - If you want to only install the packages needed for the base bot, see :ref:`getting_started/bot:packages`.

-  If you haven't already, create the bot on Discord's side and get its token with the :ref:`section above <getting_started/bot:discord's side>`.

-  Use the token to fill the :envvar:`DISCORD_TOKEN` variable in ``.env.example``. If you haven't already,
   set the other variables :ref:`mentionned above <getting_started/bot:env variables>`.

-  Rename ``.env.example`` to ``.env``.

   .. warning::
      This step is important. Normally, not renaming the file means the bot won't be able to find it and will fail
      starting up. Even if it doesn't, you should still rename it since it may get overwritten when updating
      the bot with ``git pull``. That's why the ``.example`` extension was added.

-  Add the bot to a server: for instructions :ref:`see above <getting_started/bot:adding it to a server>`.

-  Then, run :py:mod:`bot.py`:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 bot.py

.. tab:: Windows

   .. code-block:: bat

      py bot.py

Using cogs
----------

Cogs are like extensions to the bot, and contain most of its commands.
To find out more about them and how to use them, see :doc:`./../cogs/intro-cogs`.
