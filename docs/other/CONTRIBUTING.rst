:orphan:

Contributing to CroissantBot
============================

First off, thank you for considering contributing to CroissantBot! :)

The following is a set of guidelines for contributing to the repository.
These are guidelines, not hard rules.

-  `This is too much to read, I just want to ask a
   question! <#this-is-too-much-to-read-i-just-want-to-ask-a-question>`__
-  `What type of contributions are
   allowed? <#what-type-of-contributions-are-allowed>`__
-  `Your first contribution <#your-first-contribution>`__
-  `Code guidelines <#code-guidelines>`__

   -  `Command example <#command-example>`__
   -  `Docstring example <#docstring-example>`__
   -  `Being explicit <#being-explicit>`__

-  `Contributing code <#contributing-code>`__
-  `Code review process <#code-review-process>`__
-  `Reporting bugs <#reporting-bugs>`__

   -  `Security disclosures <#security-disclosures>`__
   -  `Regular bugs <#regular-bugs>`__

-  `Suggesting a feature or
   enhancement <#suggesting-a-feature-or-enhancement>`__
-  `Questions and other issues <#questions-and-other-issues>`__

This is too much to read, I just want to ask a question!
--------------------------------------------------------

You can `open an
issue <https://github.com/JulioLoayzaM/CroissantBot/issues>`__ and use
the ``question`` label.

What type of contributions are allowed?
---------------------------------------

All contributions are welcome: share suggestions, feature ideas and bug
reports by `opening an
issue <https://github.com/JulioLoayzaM/CroissantBot/issues>`__.

Code contributions are also welcome, fork the repo and `create a pull
request <https://github.com/JulioLoayzaM/CroissantBot/pulls>`__.

See below for more information.

Your first contribution
-----------------------

You want to contribute but don't know where to start? You can check:

-  The `good first issue
   label <https://github.com/JulioLoayzaM/CroissantBot/labels/good%20first%20issue>`__,
   for issues that usually require just a few lines of code and where steps towards the solution are provided.
-  The `help wanted
   label <https://github.com/JulioLoayzaM/CroissantBot/labels/help%20wanted>`__,
   for issues that require more attention and/or time, but aren't necessarily harder than first issues.

Working on your first pull request? Check out `this guide <https://opensource.guide/how-to-contribute/>`__.
If you still have some doubts, feel free to ask for help. :)

Code guidelines
---------------

Some things to consider before submitting code:

1. Document and comment your code (examples below):

   -  Commands must have the ``name`` and ``help`` fields, even if the
      function and command have the same name.
   -  In general, functions must be type-hinted and have a clear
      description in its docstring.
   -  Don't hesitate to comment: if there are too many (unnecessary)
      comments, they can be cleaned before merging.
   -  Remember, `explicit is better than
      implicit <https://www.python.org/dev/peps/pep-0020/#the-zen-of-python>`__:
      descriptive names should be used, one-liners should be avoided.
   -  Use tabs.

2. Test your changes if possible.
3. Begin your commit message with an action in the present tense:
   add \| remove \| change \| fix \| deprecate.

Command example
~~~~~~~~~~~~~~~

Using the ``@command`` decorator, we have:

.. code:: python

    @bot.command(
        name="ping",
        help="Pings the bot"
    )
    async def ping_back(ctx: commands.Context):
        pass

This defines its name instead of using the function's name. It allows to
have an explicit function name while using a short, easy-to-remember
word as a command name.

This also defines the help text instead of using the docstring.
This is visible to the bot's users, so it should be a single phrase explaining the command's purpose,
while the docstring, visible to developpers, should have a description of the function's inner workings.

Docstring examples
~~~~~~~~~~~~~~~~~~

For cogs
^^^^^^^^

Since cogs can't be properly documented using :program:`sphinx` (due to the use of decorators),
we use a simpler format for docstrings:

.. code-block:: python

   def is_even(self, n: int) -> bool:
      """
      # The first lines explain the function's purpose.
      Checks if an integer is even.

      # A list of parameters/arguments.
      Parameters:
         n: The integer to check.

      # The errors raised, if any.
      Raises:
         TypeError if n is not an integer.

      # The returned value or values.
      Returns:
         True if n is even, False otherwise.
      """

For ext modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :ref:`ext/ext-modules:ext modules` provide extensions used by the cogs, but that don't necessarily
rely on them. This means anyone wanting to customize their bot (eg. add commands) should be able
to use these modules to extend the bot's functionnality.

As such, and since they don't use decorators, these modules are documented using :program:`sphinx-autodoc`,
so their docstrings must use a certain format, shown below:

Taken from ``queue.insert``:

.. code:: python

   def insert(self, song: Song, index: int) -> str:
      """
      Inserts a song at position index.

      :param song:
         The song to insert.
      :type song: Song

      :param index:
         The index of the position to insert the song into.
      :type index: int

      :raises IndexError:
         If index is out of range.

      :return:
         A message about the result of the operation.
      :rtype: str
      """

In both cases
^^^^^^^^^^^^^

We see that the function:

-  Is type-hinted, i.e. the type of the parameters and the return values
   are indicated.
-  Has a description of its behaviour.
-  Explains the different parameters, return values, and possible
   exceptions, whenever it applies.
-  The exceptions to this are the :py:attr:`self` and the :py:attr:`ctx` parameters,
   since they are heavily used and specifying their use is not needed.

Type-hinting outside of docstrings is encouraged, especially for
imported classes, since IDEs usually use it to show suggestions.

Being explicit
~~~~~~~~~~~~~~

In :py:func:`bot.check_token`, we use two different URLs: instead of calling
them :py:attr:`url1` and :py:attr:`url2`, we use descriptive names like
:py:attr:`validate_url` and :py:attr:`token_url`.

Contributing code
-----------------

The following guide was adapted from
https://github.com/MarcDiethelm/contributing/blob/master/README.md:

-  Create a personal fork of the project on GitHub.
-  Clone the fork on your local machine. Your remote repo on GitHub is
   called ``origin``.
-  Add the original repository as a remote called ``upstream``.
-  If you created your fork a while ago be sure to **pull upstream
   changes** into your local repository.
-  Create a new branch to work on! Branch from ``develop``, preferably
   with a distinctive name such as ``develop/translation``.
-  Implement/fix your feature, comment your code.
-  Follow the code style of the project: see the `code
   guidelines <#code-guidelines>`__.
-  Add or change the documentation as needed.
-  Squash your commits with git's `interactive
   rebase <https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase>`__.
   Create a new branch if necessary.
-  Push your branch to your fork on GitHub, the remote ``origin``.
-  From your fork open a pull request in the ``develop`` branch.
-  …
-  If the maintainer requests further changes just push them to your
   branch. The PR will be updated automatically.
-  Once the pull request is approved and merged you can pull the changes
   from ``upstream`` to your local repo and delete your extra
   branch(es).

For more information on the related commands, you can check this gist:
https://gist.github.com/adamloving/5690951.

Code review process
-------------------

I will review all submitted code, as soon as possible. If after giving
feedback and a reasonable delay has passed, no response is given, I will
consider closing the pull request.

All tags/releases are to be signed by me.

Reporting bugs
--------------

Security disclosures
~~~~~~~~~~~~~~~~~~~~

If you find a security issue, **do not open an issue**. Email me at
croissantbot [dot] jlm [at] gmail [dot] com.

Regular bugs
~~~~~~~~~~~~

Create an issue using the bug template and fill it with as much detail
as possible.

Create a pull request if you have found a fix!

Suggesting a feature or enhancement
-----------------------------------

Create an issue using the feature request template and fill it with as
much detail as possible.

Create a pull request if you have already started implementing it!

Questions and other issues
--------------------------

Issue templates are only available for bug reports and features requests
for the moment, so don't hesitate to use a blank issue if your question
doesn't belong to those categories.
