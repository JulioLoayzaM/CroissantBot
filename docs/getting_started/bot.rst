Running the bot
===============

A guide on how to create and run the bot.

Intro
-----

-  CroissantBot's main file is aptly named :py:mod:`main.py`.
   It start the tasks required to run the bot and loads the ``base`` cog.
   This includes the ``exit``, ``help``, ``ping``, ``test`` and ``version`` commands.

-  The bot uses cogs, which are kind of like plugins, to add commands by categories.
   Some require additional setup (for example, an API token), so not all cogs are enabled by default.
   For more information, see :ref:`cogs/intro-cogs:intro to cogs`.

-  CroissantBot uses a file called ``.env`` to store its settings and credentials.

.. versionadded:: 3.0.0
   A configuration script, ``config.py``, is provided to ease the first setup of the bot.

Dependencies
------------

This a list of all the packages used by the bot and its cogs.
You can install all of them with the instructions below, or check which ones
are actually needed by the commands you want to use.

.. Version 2 was tested with Python 3.6.9 in Ubuntu 18.04 and Python 3.6.1 in Windows 10 using the following packages:

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


Creating the bot
----------------

First, you have to create an application on Discord, in order to create a bot
and get its token.

Creating the application
^^^^^^^^^^^^^^^^^^^^^^^^

To create the application and the bot, I recommend following
`this guide <https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-the-developer-portal>`_.
Here's a quick rundown of the steps to follow:

- If needed, create a Discord account and verify your email.
- Login to `Discord's developer portal <https://discord.com/developers/applications>`_.
- Create a new application.
- In the Bot section (on the left), create a bot. You can change the default name.
- Grab the token.
- Scroll down and enable the ``server members intent`` under Privileged Gateway intents.

Adding the bot to a server
^^^^^^^^^^^^^^^^^^^^^^^^^^

To add the bot to a server (a guild in the API's terminology) see
`this part <https://realpython.com/how-to-make-a-discord-bot-python/#adding-a-bot-to-a-guild>`_
of the previous guide.
Essentially:

- In the `developer portal <https://discord.com/developers/applications>`_, go to the OAuth2 tab.

- In the OAuth2 URL Generator, select *bot* in Scopes.

- As for permissions, there are two options:

  -  For a private server, Administrator is the easier choice.
  -  For a bigger or more public server, it's better to select only the permissions needed for the bot to run correctly.

For now, the permissions I'm using with the bot are:

.. list-table::
   :header-rows: 1

   * - Permissions
     -
   * - View channels
     - Send messages
   * - Embed links
     - Attach files
   * - Add reactions (not used yet)
     - Manage messages
   * - Read message history
     - Use Application Commands
   * - Connect
     - Speak
   * - Use voice activity
     -

.. note::
   You can set the bot to public, allowing anyone who has the link you generated
   to invite the bot to their server, provided they have the necessary permissions
   (`Manage server` permission).
   Or you can leave the bot as private, which means only you can use the link to
   add the bot to any server in which you have the `Manage server` permission.

Installation and setup
----------------------

Now, time to install the source code and run the bot!

-  `Clone the repo <https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository>`__
   or download the code from the
   `releases page <https://github.com/JulioLoayzaM/CroissantBot/releases>`__.

   .. note::
      Cloning the repo is recommended in order to use Git to easily update the bot.

-  Install Python 3.6+: use your package manager or head over to
   `the download page <https://www.python.org/downloads/>`__.

-  Optional but recommended: use `pipenv <https://pipenv.pypa.io/en/latest/>`__
   to avoid conflicts with the dependencies.
   Previously, I used `virtual environments <https://python.land/virtual-environments/virtualenv>`__,
   so the ``requirements.txt`` is still included.

-  To install all the package dependencies, use:

.. tab:: ``pipenv``

   .. code-block:: bash

      pipenv install

.. tab:: ``pip`` (Linux/MacOS)

   .. code-block:: bat

      python3 -m install -U -r requirements.txt

.. tab:: ``pip`` (Windows)

   .. code-block:: bat

      py -m pip install -U -r requirements.txt

-  If you haven't already, create the bot on Discord and get its token with the
   :ref:`section above <getting_started/bot:Creating the application>`.

-  Launch the configuration script and follow the instructions:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bat

      python3 config.py

.. tab:: Windows

   .. code-block:: bat

      py config.py

.. important::
   This copies the ``.env.example`` to ``.env``. This is important for two reasons:
   the bot looks for and uses the file called ``.env``,
   and when updating the bot with Git the contents of ``.env.example`` may be overwritten.

-  Add the bot to a server: for instructions
   :ref:`see above <getting_started/bot:Adding the bot to a server>`.

-  Then, run :py:mod:`main.py`:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 main.py

.. tab:: Windows

   .. code-block:: bat

      py main.py

Adding features
---------------

That's it! The bot should be running.

But just running the base bot is not really that interesting:
it barely has commands.
This is where cogs come in.
They are like extensions to the bot and contain most of its commands.
To find out more about them and how to use them, see :doc:`./../cogs/intro-cogs`.
