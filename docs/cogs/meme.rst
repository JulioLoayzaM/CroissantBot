Meme
====

This Cog enables the bot's meme-sending capabilities.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_MEME` variable.

Packages
--------

:py:mod:`asyncpraw`, the Asynchronous Python Reddit API Wrapper,
is used to get the images from Reddit.

env variables
-------------

.. csv-table::
   :file: meme-vars.csv
   :header-rows: 1
   :delim: ,

Creating a Reddit bot
^^^^^^^^^^^^^^^^^^^^^
The variables starting with :envvar:`REDDIT` correspond to a Reddit bot's credentials.
`According to its docs <https://asyncpraw.readthedocs.io/en/latest/getting_started/quick_start.html>`__,
to use :py:mod:`asyncpraw` we need:

-  A Reddit account: to create a new account, head to
   `reddit.com <https://www.reddit.com/>`__.
   You can create an account without providing an email address (just omit it),
   but be aware this means **there's no way to recover the account
   if the password is lost**.

-  A Client ID and Secret: see
   `this guide <https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps>`__.

-  A User Agent: this Cog already generates one following the format provided by
   `Reddit's API guide <https://github.com/reddit-archive/reddit/wiki/API>`__.
   Thus, I recommend letting the bot take care of that with the information provided by ``.env``.
   Note that the :envvar:`APP_VERSION` is set arbitrarily;
   I use the same version as the bot's.

.. versionadded:: 2.0.0
   The bot can send memes without downloading them (:envvar:`MEME_DOWNLOAD`).

.. versionadded:: 3.0.0
   The :envvar:`MEME_DIR` directory is created by the configuration script.

How it works
------------

List files
^^^^^^^^^^

These are the files created when the command is used for the first time in a server or DM.
They contain a list of the names of all the files sent to that server/DM.
This allows the bot to check whether a meme was already sent to that context,
and thus avoid sending duplicates.
These list files are saved in the directory pointed by :envvar:`MEME_DIR`.

Asyncpraw
^^^^^^^^^

When starting, the bot creates an :py:class:`asyncpraw.Reddit` instance.
This instance fetches the top :envvar:`MEME_ITEM_LIMIT` posts from the Hot category of a subreddit.

If the post is actually an image (not a mod post, nor a video, nor a text-only post),
it checks if it already sent it to that context (server or DM).
If it did, it skips that post and checks the next one fetched,
so it can eventually run out of posts to check.

If you use the ``meme`` command frequently with the same subreddit,
you should increase the item limit so the bot can send more new memes before reaching this cap.

Downloading memes
^^^^^^^^^^^^^^^^^

Since version 2.0.0, you can choose skip the download of the memes to send.
This uses the fact that :py:class:`discord.Embed` can use a URL to include an image directly.

You can still enable the download of the images, which are then used to send the messages.
These are saved in the directory set in :envvar:`MEME_DIR`.

A meme's filename is derived from its ``i.redd.it`` URL. For example,
from ``i.redd.it/thisisnotameme.jpg`` we get ``thisisnotameme.jpg``.
