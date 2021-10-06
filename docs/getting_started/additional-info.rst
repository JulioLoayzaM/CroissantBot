Additional info
===============

Some useful tidbits of information.

Keeping the bot online
~~~~~~~~~~~~~~~~~~~~~~

In order to continuously run the bot on my Raspberry Pi 4 I use :program:`tmux` (`<https://github.com/tmux/tmux/wiki>`__).
It can create a detachable session which keeps the program running in the background,
letting the user interact normally with the shell.
A :program:`tmux` session can be reattached to the same or a different terminal or :program:`ssh` session.

Modifying the code
~~~~~~~~~~~~~~~~~~

The idea of this template is to allow any modification to the code.
As such, the code can be freely modified under one condition:
the content of the LICENSE file must be included with all copies or substantial portions of the code.
For more information, see the :doc:`./../other/LICENSE`.
For an example on how this works, see the Music cog, which has code from the
`basic\_voice example <https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py>`__
of ``discord.py``.

Also, consider contributing your modifications to the code! :)

See :doc:`./../other/CONTRIBUTING`.