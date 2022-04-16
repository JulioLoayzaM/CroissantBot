Introduction
============

CroissantBot is a Discord bot written in Python using the `discord.py rewrite <https://github.com/Rapptz/discord.py>`__.

While the bot itself is not openly available, `its code is <https://github.com/JulioLoayzaM/CroissantBot>`_.
This project aims to be a template to ease the creation of a new bot, allowing
anyone\* to clone the repo, fill in the blanks with this documentation, and run it on their machine.

\*some Python experience is recommended, but this guide should provide the necessary to run the bot.

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
   No need to download them in order to send them.

Kill messages
~~~~~~~~~~~~~

Sends a message targeting a specified server member.
Keeps count of kills in each server.
Messages not included.

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