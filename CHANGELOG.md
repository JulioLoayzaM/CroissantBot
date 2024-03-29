# Changelog

## CroissantBot 3.0.0 (2022-12-20)

CroissantBot's second major update!

After being a WIP for months, I can finally say that CroissantBot works with
discord.py 2.0.0! :)

This update brings the `config.py` script to make the initial configuration a
bit easier. The rest mainly focuses on cleaning up the code and the documentation,
so there aren't many new shiny features.

### Version 3.0.0 highlights
- Added a new configuration script:
  the previous version relied a lot on users reading a good part of the documentation just to get the bot running.
  Now, `config.py` takes care of a lot of small configuration steps that weren't important to the user.
- Added a new main file: separates the custom Bot class from the code that actually runs it.
- **Breaking**: with this new update some `.env` vars were changed.
  Most notably, the bot token variable `DISCORD_TOKEN` is now called `BOT_TOKEN`.
- **Breaking**: The bot no longer uses `yt-dl`, just `yt-dlp`.
- Instead of using `venv` I now use `pipenv`. The `requirements.txt` is still maintained,
  but will probably be removed at some point in the future.
- The English version of the documentation was updated, but the Spanish version was not.
  As I don't know if anyone is using the bot, let alone with the Spanish documentation,
  it makes little sense to continue translating everything. That being said, if you use
  this bot with the Spanish docs don't hesitate to create issues.

### Patch notes
A couple of changes worth mentioning:
- Override the env vars, so that changes to `.env` are applied when using `pipenv`.
- Fixed a bug where the bot only searched the first word it was given when using the `play` command.

## CroissantBot 2.0.0 (2021-11-10)

CroissantBot's first major update!

Now with playlists managed with PostgreSQL, the option to select which cogs to use and a big documentation overhaul.

### Version 2.0.0 highlights

- The big documentation overhaul: the docs are now hosted by Read the Docs, you can find them [here](https://croissantbot.readthedocs.io/en/latest/). As such, the documentation now uses reStructuredText instead of Markdown.

- Added playlists! They come in two flavours now:
  - The Playlist cog, which uses a PostgreSQL database to maintain as many playlists as you want.
  - The Favourites commands, introduced in version 1.1.0, are now in their own cog. It can only hold one playlist per user but doesn't require anything other than a simple JSON file.
  - Note that one doesn't interfere with the other, but they aren't synchronised either.
- Added the option to select which cogs to load through variables in the `.env` file.
- Added an option to enable/disable the download of memes. Memes can still be sent, but no local copy will be made if the option is disabled.
- Removed the `play_from` command.
- Added a `reload` command to reload a cog while running the bot. This is useful to test changes to a cog without having to restart the bot.

### Patch notes

There are a ton of commits related to the new Playlist cog that won't be mentioned here. Some notes:

- When adding a song to a playlist, if the playlist doesn't already exist, it is created. This means that typos in the name can lead to extra playlists.
- The `DatabaseConnection` classes are documented, with the intention to allow others to use them to add features to the Playlist cog.
- Related to the previous item, Queue and Song are documented too.
- And to expand on this, all other Python files have a new documentation style, which should be easier to read and renders better on VSCode's hints.
- The Meme cog now saves its Reddit session instead of opening a new one each time a meme is requested.
- The item limit of the Meme cog is now a `.env` variable, and a command was added to easily change it while running.
- A unit test was added for the Queue module, to ensure the transition from using a List to a Deque works and to learn about `pytest`.

## CroissantBot 1.1.2 (2021-09-28)

Source code met `flake8`, `ping` now shows latency, guild names are now logged.

### Patch notes

- added: using `ping` when the bot is connected to a voice channel shows its latency.
- added: `on_guild_join`, logs any newly joined guild.
- added: `on_ready` now logs the list of currently joined guilds.
- added: `exit` now sends a message before closing the bot.
- changed: every `.py` file has gone through `flake8`.

## CroissantBot 1.1.1 (2021-09-22)

Small fix for `version`, better `ping`.

### Patch notes

- fixed: last version's notes were so long, they didn't fit in an Embed's field!
  - fix: Now `version remote` only shows the message before the notes.
  - add: The full notes can be shown with `version notes`.
- changed: the `ping` command now returns the latency.
- changed: the `play_from` and `poggers` command are now hidden.

## CroissantBot 1.1.0 (2021-09-21)

CroissantBot's first minor version update!

Now, the `play` command is all you need to play music, and can even tell the bot to join your voice channel! `yt-dlp` begins to replace `youtube-dl` but since it's a [minor version](https://semver.org/#spec-item-7), backwards compatibility is maintained.

And thanks to Troy Sherlock and SURAJITSHAW for their contributions. :)

### Version 1.1.0 highlights

Julio Loayza - @JulioLoayzaM:

- added: `favourites` group of commands to manage a list of favourite songs.
  - See the list of commands in [commands.md](docs/commands.md#favourites-subcommands) and more info about the file used in [music.md](docs/music.md).
- added: `yt-dlp` to replace `youtube-dl`.
  - changed: the `youtube` cog now uses `yt-dlp` (or `youtube-dl`) to get a stream's title and thumbnail.
  - deprecated: `youtube-dl`, but backwards compatibility is maintained for the time being.
  - More info: [README](README.md#dependencies), [music.md](docs/music.md#requirements) and [youtube.md](docs/youtube.md#requirements).
- added: `ensure_voice` to auto-connect the bot to a voice channel when using `play`.
- added: 'Code of Conduct' and 'Código de Conducta'.

Troy Sherlock - @TroySherlock:

- changed: merged `play` and `play_from` commands into `play` (#2).
  - deprecated: the `play_from` command.
- added: `validate_url` to check if a `play` query is a URL.

SURAJITSHAW - @SURAJITSHAW:

- changed: `Twitch.check_users` is now `async`, `streamlink.streams` is run with `run_in_executor` (#4).

### Patch notes

Julio Loayza - @JulioLoayzaM:

- changed: `Music.play` YouTube search is run with `run_in_executor`.
- changed: using `aiofiles.open` when possible.
- changed: better list of steps to follow in CONTRIBUTING.
- changed: pull request and issues templates.

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

- fixed: a fatal error that occurred when `TW_TOKEN` could not be refreshed
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
