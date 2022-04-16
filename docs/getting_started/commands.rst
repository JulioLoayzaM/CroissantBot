Commands
========

The lists of all available commands.

When running the bot you can use the ``help`` command to get a list of all available commands *in the
current context*: some commands are guild-only, meaning they can't be
used in DMs (eg. music commands). Others can only be used by the bot's
owner (eg. ``exit`` to stop the bot).

Base
~~~~

.. list-table::
   :header-rows: 1

   * - Commands
     - Aliases
     - Description
     - Comments
   * - ``exit``
     -
     - Closes the bot
     - Owner-only
   * - ``ping``
     -
     - Pings the bot
     -
   * - ``reload``
     -
     - Reload a cog
     - Owner-only
   * - ``version``
     - ``ver``
     - Check the current version, can check the latest remote version
     - Owner-only

Meme
~~~~

.. list-table::
   :header-rows: 1

   * - Command
     - Aliases
     - Description
     - Comments
   * - ``meme``
     -
     - Sends a meme from a subreddit, r/memes by default.
     -
   * - ``change_meme_limit``
     -
     - Change the maximum number of items to fetch from a subreddit
     - Default: 10

Misc
~~~~

.. _croissant-command:
.. list-table::
   :header-rows: 1

   * - Command
     - Aliases
     - Description
     - Comments
   * - ``croissant``
     -
     - Sends a gif
     - 🥐
   * - ``kill``
     -
     - Kill your enemies (and your friends)
     - Guild-only
   * - ``kill_count``
     - ``count``, ``kc``
     - Shows your kill count, can specify a user to check your stats against them
     - Guild-only

Music
~~~~~

.. note:: All music commands are guild-only.

.. versionadded:: 1.1.0
   The bot can join your voice channel automatically when using ``play``.

.. deprecated:: 1.1.0
   The ``play_from`` command.

.. list-table::
   :header-rows: 1

   * - Command
     - Aliases
     - Help
   * - ``join``
     - ``j``
     - Tells the bot to join your current voice channel.
   * - ``leave``
     -
     - Tells the bot to disconnect from its current voice channel
   * - ``move``
     - ``m``
     - Moves a song's position in the queue
   * - ``move_here``
     - ``mh``
     - Moves the bot to your voice channel if the bot's current channel is empty
   * - ``now_playing``
     - ``now``
     - Displays the currently playing song
   * - ``pause``
     -
     - Pauses the currently playing song
   * - ``play``
     - ``p``
     - Plays a song from a URL or a search query
   * - ``remove``
     -
     - Removes a song from the queue through its ``index``, 0 means no song is selected
   * - ``resume``
     - ``res``
     - Resumes a paused song
   * - ``search_youtube``
     - ``yt``, ``youtube``
     - Shows a list of the top 5 results of your search from youtube
   * - ``show_queue``
     - ``q``, ``queue``
     - Displays the current queue
   * - ``skip``
     - ``s``
     - Skips ``index`` number of songs, 1 by default
   * - ``stop``
     -
     - Stops the currently playing (or paused) song and clears the queue
   * - ``volume``
     - ``vol``
     - Changes the volume, range: 0-100

Favourites
~~~~~~~~~~

.. versionadded:: 1.1.0

.. list-table::
   :header-rows: 1

   * - Command
     - Description
     - Comment
   * - ``favourites``
     - Base command for managing favourite songs
     - Alias: ``fav``
   * - ``list``
     - Displays your list of favourites: if an index is specified, shows that song's info
     - Subcommand
   * - ``add``
     - Saves a song to your list from its URL
     - Subcommand
   * - ``remove``
     - Removes a song from your list by its index, 0 means no song is removed
     - Subcommand
   * - ``now``
     - Saves the currently playing song to your list
     - Subcommand, guild-only
   * - ``play``
     - Plays a song from your list by its index
     - Subcommand, guild-only

Playlist
~~~~~~~~

.. versionadded:: 2.0.0

.. csv-table::
   :file: commands-playlist.csv
   :header-rows: 1
   :delim: ,