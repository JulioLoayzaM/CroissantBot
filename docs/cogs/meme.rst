Meme
====

This Cog enables the bot's meme-sending capabilities.
It uses :py:mod:`asyncpraw`, or the Asynchronous Python Reddit API Wrapper, to get images from Reddit.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_MEME` variable.

Requirements
------------

Packages
^^^^^^^^

-  The :py:mod:`asyncpraw` package:

.. tab:: Unix (Linux/MacOS)

   .. code-block:: bash

      python3 -m install -U asyncpraw

.. tab:: Windows

   .. code-block:: bat

      py -m pip install -U asyncpraw

env variables
^^^^^^^^^^^^^

-  Create a directory to store the :ref:`cogs/meme:list files` and set :envvar:`MEME_DIR` accordingly.

-  :envvar:`MEME_ITEM_LIMIT` indicates how many memes the bot can retrieve at once. See :ref:`cogs/meme:how it works`
   below for an explanation on how that works. The default is 10 items.

-  The variables starting with :envvar:`REDDIT` correspond to a Reddit bot's credentials. `According to the docs
   <https://asyncpraw.readthedocs.io/en/latest/getting_started/quick_start.html>`__,
   to use :py:mod:`asyncpraw` we need:

   -  A Reddit account: to create a new account, head to
      `reddit.com <https://www.reddit.com/>`__. You can create an account
      without providing an email address (just omit it), but be aware this
      means **there's no way to recover the account if the password is
      lost**.

   -  A Client ID and Secret: see `this
      guide <https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps>`__.

   -  A User Agent: this Cog already generates one following the format
      provided by `Reddit's API
      guide <https://github.com/reddit-archive/reddit/wiki/API>`__. Thus, I
      recommend letting the bot take care of that with the information
      provided by ``.env``. Note that the :envvar:`APP_VERSION` is set
      arbitrarily; I use the same version as the bot's.

.. versionadded:: 2.0.0

-  You can decide whether to download the memes or just send them using their URL by setting the :envvar:`MEME_DOWNLOAD`
   variable. To turn off downloads, leave the variable commented or set it to a
   `falsy value <https://www.freecodecamp.org/news/truthy-and-falsy-values-in-python/>`__.
   To turn it on, set it to a truthy value.

How it works
------------

List files
^^^^^^^^^^

These are the files created when the command is used for the first time in a server or DM.
They contain a list of the names of all the files sent to that server/DM.
This allows the bot to check whether a meme was already sent to that context, and thus avoid sending duplicates.
These list files are saved in the directory pointed by :envvar:`MEME_DIR`.

Asyncpraw
^^^^^^^^^

When starting, the bot creates an :py:class:`asyncpraw.Reddit` instance.
This instance fetches the top :envvar:`MEME_ITEM_LIMIT` posts from the Hot category of a subreddit.
If the post is actually an image (not a mod post, nor a video, nor a text-only post),
it checks if it already sent it to that context (server or DM).

If it did, it skips that post and checks the next one fetched.
So it can eventually run out of posts to check.

If you use the ``meme`` command frequently with the same subreddit, you should increase the item limit
so the bot can send more new memes before reaching this cap.

Downloading memes
^^^^^^^^^^^^^^^^^

Since version 2.0.0, you can choose skip the download of the memes to send.
This uses the fact that :py:class:`discord.Embed` can use a URL to include an image directly.

You can still enable the download of the images, which are then used to send the messages.
These are saved in the directory set in :envvar:`MEME_DIR`.

A meme's filename is derived from its ``i.redd.it`` URL. For example,
from ``i.redd.it/thisisnotameme.jpg`` we get ``thisisnotameme.jpg``.
