Intro to cogs
=============

What are cogs?
--------------

Cogs are ``discord.py`` classes that allow bot developers to group commands.
For example, the code for the music commands can be found in the Music cog.
These cogs are loaded when the bot is starting up, which means we could tell CroissantBot
what to load.

Since version 2.0.0, cogs are *not* enabled by default.
Instead, you can choose what to use or not, like plugins.
This means you don't have to set up cogs you won't use.

Enabling cogs
-------------

As explained in :ref:`this section <getting_started/bot:intro>`, CroissantBot uses a file called ``.env``
to store the various credentials it uses and its configuration.
Particularly, the :envvar:`ENABLE_\<cog\>` variables are used to determine what cogs should be loaded.

To enable a cog, uncomment and set the corresponding variable to any
`truthy value <https://stackoverflow.com/questions/39983695/what-is-truthy-and-falsy-how-is-it-different-from-true-and-false>`_.
Basically, leave it as ``"ON"`` or set it to any string that is **not** empty.

.. attention::
   Enabling some cogs but not others can lead to some limited functionnality. For example,
   disabling the Music cog means that you can't play music using the Playlist commands.

Setting up cogs
---------------

But that's not it! As you may have noticed, there are *many* variables below the :envvar:`ENABLE` ones.

All cogs use at least one ``.env`` variable for things ranging from getting API credentials to getting the path
to a file they need. So to actually use a cog, you have to set it up. That's where the following guides come in handy.

Each one explains the packages needed by each cog (in case you didn't install them all already using the ``requirements`` file),
so you know which ones you can skip if you're installing them one by one.
They also explain what their corresponding ``.env`` variables are and what to set them to.

The Meme and the Twitch cogs require an account in a third-party service (Reddit and Twitch respectively).
The only way to skip this is by not using these cogs.
