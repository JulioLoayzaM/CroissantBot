# Changelog

## CroissantBot 1.0.5 (2021-09-10)

CONTRIBUTING and docstrings overhaul.

### Patch highlights

- added: CONTRIBUTING, and its Spanish version CONTRIBUIR.
- added: pull requests, bug reports and feature requests templates.
- added: table of contents to README and LEEME.
- added: reference to CONTRIBUTING and CONTRIBUIR in README and LEEME respectively.
- updated: docstrings overhaul to adhere to the new code guidelines set in CONTRIBUTING.
- fixed: created `bot.create_session` to avoid `aiohttp`'s DeprecationWarning for not creating the session with `async`.

## CroissantBot 1.0.4 (2021-09-09)

The `async` patch, featuring `aiohttp` and `aiofiles`.

### Patch highlights

- updated: moved `bot.py` from `requests` to `aiohttp`
- updated: moved `bot.check_version` from `subprocess` to `asyncio.subprocess`
- updated: meme cog now creates just one `aiohttp.session`
- added: snippet to close meme cog's `aiohttp.session` during bot exit
- updated: twitch cog now receives `aiohttp.session` from `bot.check_twitch`
- removed: `bot.close_connection` part that closed `twitch.session`
- updated: `twitch.check_users` is now asynchronous
- updated: reading `KILL_MESSAGES` is now asynchronous
- updated: checking the list_file and downloading memes in `meme.get_meme` are now asynchronous

## CroissantBot 1.0.3 (2021-09-07)

Logs and versions.

### Patch highlights

- added: time-rotating logs, with a rollover at midnight
- added: `LOG_COUNT` to indicate how many days of logs to keep
- added: small section on `bot.md` about logs
- updated: better embeds for `check_version` (new format + colour-coded)
- fixed: an error caused by a missing continue when `streamlink` raises a `PluginError`

## CroissantBot 1.0.2 (2021-09-05)

The Spanish patch. :)

### Patch highlights

- added: Spanish version of docs, LICENSE and README
- added: reference to Spanish version in README
- updated: improvements to the docs
- updated: `streamlink.PluginError` is now logged with `streamlink.plugin.youtube` to `streamlink.log`

## CroissantBot 1.0.1 (2021-09-05)

CroissantBot's first patch!

### Patch highlights

- fixed: a fatal error that occured when `TW_TOKEN` could not be refreshed
- added: more info is logged when `TW_TOKEN` is invalid

## CroissantBot 1.0.0 (2021-09-04)

CroissantBot's first release!

Since it's the first release, there are no changes to log. :)

Instead here's a recap of the current features and what comes next:

### Features

- Play music from YouTube
- Send memes from Reddit
- Send funny death messages
- Check for new Twitch and YouTube livestreams
- Logging to monitor bot's behaviour

### What comes next

I plan to keep working on this bot: check the [TODO](README.md#to-do) and [Considering](README.md#Considering) sections of the README file to see the changes I'm planning on implementing.