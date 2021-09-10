# Contributing to CroissantBot

First off, thank you for considering contributing to CroissantBot! :)

The following is a set of guidelines for contributing to the repository. These are guidelines, not hard rules.

- [This is too much to read, I just want to ask a question!](#this-is-too-much-to-read-i-just-want-to-ask-a-question)
- [What type of contributions are allowed?](#what-type-of-contributions-are-allowed)
- [Your first contribution](#your-first-contribution)
- [Code guidelines](#code-guidelines)
	- [Command example](#command-example)
	- [Docstring example](#docstring-example)
	- [Being explicit](#being-explicit)
- [Contributing code](#contributing-code)
- [Code review process](#code-review-process)
- [Reporting bugs](#reporting-bugs)
	- [Security disclosures](#security-disclosures)
	- [Regular bugs](#regular-bugs)
- [Suggesting a feature or enhancement](#suggesting-a-feature-or-enhancement)
- [Questions and other issues](#questions-and-other-issues)

## This is too much to read, I just want to ask a question!

You can [open an issue](https://github.com/JulioLoayzaM/CroissantBot/issues) and use the `question` label.

## What type of contributions are allowed?

All contributions are welcome: share suggestions, feature ideas and bug reports by [opening an issue](https://github.com/JulioLoayzaM/CroissantBot/issues).

Code contributions are also welcome, just fork the repo and [create a pull request](https://github.com/JulioLoayzaM/CroissantBot/pulls).

See below for more information.

## Your first contribution

You want to contribute but don't know where to start? You can check:

- the [`good first issue` label](https://github.com/JulioLoayzaM/CroissantBot/labels/good%20first%20issue), for issues that usually require just a few lines of code.
- the [`help wanted` label](https://github.com/JulioLoayzaM/CroissantBot/labels/help%20wanted), for issues that require more attention, but aren't necessarily harder than first issues.

Working on your first pull request? Check out [this guide](https://opensource.guide/how-to-contribute/). If you still have some doubts, feel free to ask for help. :)

## Code guidelines

Some things to consider before submitting code:

1. Document and comment your code (examples below):
   - Commands must have the `name` and `help` fields, even if the function and command have the same name.
   - In general, functions must be type-hinted and have a clear description in its docstring.
   - Don't hesitate to comment: if there are too many (unnecessary) comments, they can be cleaned before merging.
   - Remember, [explicit is better than implicit](https://www.python.org/dev/peps/pep-0020/#the-zen-of-python): descriptive names should be used, one-liners should be avoided.
2. Test your changes.
3. Begin your commit message with an action: added|removed|updated|fixed.

### Command example

Using the `@command` decorator, we have:

```python
@bot.command(
	name="ping",
	help="Pings the bot"
)
async def ping_back(ctx: commands.Context):
```

This defines its name instead of using the function's name. It allows to have an explicit function name while using a short, easy-to-remember word as a command name.

This also defines the help text instead of using the docstring. 'help' should be a single phrase explaining the command's purpose, while the docstring should have a description of the function's inner workings, as shown in the next example.

### Docstring example

Taken from `queue.insert`:

```python
def insert(self, song: Song, index: int) -> str:
	"""
	Inserts a song at queue[index].
	
	Parameters:
		- song: the song to be inserted.
		- index: the index on the list to insert to, as passed by the user.
	Returns:
		- a message about the result of the operation.
	Raises:
		- IndexError if index is out of range.
	"""
```

We see that the function:

- Is type-hinted, i.e. the type of the parameters and the return values are indicated.
  - The only exception, here and on the rest of the code, is the `self` parameter. If the function doesn't return values, just omit it.
- Has a description of its behaviour.
- Explains the different parameters, return values, and possible exceptions, whenever it applies.
  - The exceptions to this are the `self` and the `ctx` parameters, since they are heavily used and specifying their use is not needed.

Type-hinting outside of docstrings is encouraged, especially for imported classes, since IDEs usually use it to show suggestions.

### Being explicit

In `bot.check_token`, we use two different URLs: instead of calling them `url1` and `url2`, we use descriptive names like `validate_url` and `token_url`.

## Contributing code

For something that is bigger than a one or two line fix:

1. Fork the code.
2. Make changes in your fork, preferably in a new branch (eg. `translation`).
3. When the changes include code, make sure to adhere to the [code guidelines](#code-guidelines) and to test your code.
4. If everything looks fine, create a pull request and wait for review.

Else, you should be able to edit a file directly on GitHub.

## Code review process

I will review all submitted code, as soon as possible. If after giving feedback and a reasonable delay has passed, no response is given, I will consider closing the pull request.

All tags/releases are to be signed by me.

## Reporting bugs

### Security disclosures

I'm not expecting to deal with security issues, but if you do find one, create an issue with the title '[security] contact required' and **do not** post any info about it.

### Regular bugs

Create an issue using the bug template and fill it with as much detail as possible.

Create a pull request if you have found a fix!

## Suggesting a feature or enhancement

Create an issue using the feature request template and fill it with as much detail as possible.

Create a pull request if you have already started implementing it!

## Questions and other issues

Issue templates are only available for bug reports and features requests for the moment, so don't hesitate to use a blank issue if your question doesn't belong to those categories.