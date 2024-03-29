Misc
====

This Cog contains miscellaneous commands.

.. hint::
   To enable this cog, set the :envvar:`ENABLE_MISC` variable.

Packages
--------

No package is required!

env variables
-------------

.. csv-table::
   :file: misc-vars.csv
   :header-rows: 1
   :delim: ,

Use your own messages
---------------------

:envvar:`KILL_PATH` is a ``txt`` file which contains all the possible messages to send.
There should be only one message per line.
To insert the nickname of the user using the command, put ``<killer>`` in the message.
Likewise, to insert the victim's nickname, use ``<victim>``.
These tags are automatically replaced before sending the message.
You can put as many of these per message as you want, or none at all.
For example, if Alice calls the command on Bob, the phrase:

.. set to html to have the syntax highlighting
.. code-block:: html

   <killer> shot <victim>.

becomes:

.. code-block::

   Alice shot Bob.

How the count is stored
-----------------------

:envvar:`KILL_COUNT` is a JSON file that keeps track of how many times a
user used the command on someone on that server. When creating the
bot it should at least contain an empty dictionary ``{}``. It uses
the following format:

.. code-block:: json

   {
      "guild_id": {
            "killer_id_1": {
               "victim_id_1": 3,
               "victim_id_2": 10
            },
            "killer_id_2": {
               "victim_id_3": 14,
               "victim_id_1": 2
            }
      }
   }

.. note::
   Since the :envvar:`KILL_COUNT` file uses a server's ID as the first key, the counts are not synchronized across servers.

Croissant?
----------
:envvar:`CROISSANT_PATH` points to ``croissant.gif``,
which is the gif sent when using the :ref:`croissant command <croissant-command>`.
See the :ref:`README <index:origin>` for more information on this command's existence.
