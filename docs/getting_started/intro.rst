Introduction
============

CroissantBot is a Discord bot written in Python using the `discord.py rewrite <https://github.com/Rapptz/discord.py>`__.

While the bot itself is not openly available, `its code is <https://github.com/JulioLoayzaM/CroissantBot>`_.
This project aims to be a template to ease the creation of a new bot, allowing
anyone\* to clone the repo, fill in the blanks with this documentation, and run it on their machine.

\*some Python experience is recommended, but this guide should provide the necessary to run the bot.

.. attention::

   The development of `discord.py has ended <https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1>`__,
   in part due to the new ``Message.content`` privileged intent. According to `this Discord dev
   post <https://support-dev.discord.com/hc/en-us/articles/4404772028055-Message-Content-Access-Deprecation-for-Verified-Bots>`__,
   this new privileged intent (a permission to read messages, manually granted by Discord) should not be a problem for "Unverified bots in
   fewer than 100 servers".

   Still, any change to the API won't be reflected in ``discord.py``, so I'm currently waiting for the dust to settle to see if/when a viable
   fork emerges. For now, I'll continue working on this bot as if nothing happened.

Features
--------

.. tip::
   For a list of all commands, check :ref:`getting_started/commands:commands`.

Music player
~~~~~~~~~~~~

Play music from YouTube in voice chat. Supports playback on different
servers simultaneously, with a queue for each one.

.. versionadded:: 1.1.0
   You can save your favourite songs in one playlist, with minimal setup.
   See :ref:`cogs/favourites:favourites`.

.. versionadded:: 2.0.0
   Use a PostgreSQL database to store as many playlists as you want.
   See :ref:`cogs/playlist:playlist`.

Memes
~~~~~

Get memes from Reddit. Keeps track of memes sent to each server to avoid
duplicates.

.. versionadded:: 2.0.0
   No need to download them to send them.

Kill messages
~~~~~~~~~~~~~

Sends a message targeting a specified server member. Keeps count of
kills in each server. Messages not included.

Livestream status
~~~~~~~~~~~~~~~~~

Sometimes Twitch's notifications are unreliable, so the bot can notify
users about new streams through DMs. It works with YouTube streams as
well.

Logging
~~~~~~~

Outputs basic information and errors to ``stdout``. Debug information is
logged to a file. It should allow to at least pinpoint which function
has caused an error.