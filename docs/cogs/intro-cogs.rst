Intro to cogs
=============

What are cogs?
--------------

Cogs are ``discord.py`` classes that allow bot developers to group commands.
For example, the code for the music commands can be found in the Music cog.
These cogs are loaded when the bot is starting up, which means we can tell CroissantBot
what to load.

Since version 3.0.0, cogs are *not* enabled by default,
except for the Misc cog, as a way to show how to enable them.
This way, you can choose which one to use, and avoid setting up cogs you won't use.

Enabling cogs
-------------

CroissantBot uses a file called ``.env`` to store the various credentials it uses.
It also stores some configuration options, such as the :envvar:`ENABLE_\<cog\>` variables
used to determine which cogs are loaded on startup.

To enable a cog, uncomment and set the corresponding variable to any
`truthy value <https://stackoverflow.com/questions/39983695/what-is-truthy-and-falsy-how-is-it-different-from-true-and-false>`_.
Basically, leave it as ``"ON"`` or set it to any string that is **not** empty.

Setting up cogs
---------------
Some cogs work out-of-the-box, meaning you just have to set their :envvar:`ENABLE` variable
to use it, while others require additional setup or information.

This is why each cog has its own page in this guide.
They show the packages needed by the cog (if you don't want to install all of them)
as well as how to set their ``.env`` variables.

.. attention::
   The Meme and Twitch cogs require an account in a third-party service (Reddit and Twitch respectively).
   The only way to skip this is by not using these cogs.
