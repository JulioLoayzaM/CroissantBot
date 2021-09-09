# CroissantBot

<p align="center">
    <a href="//www.python.org/"><img src="https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54"></a>
    <a href="//github.com/JulioLoayzaM/CroissantBot/releases"><img src="https://img.shields.io/github/v/release/JulioLoayzaM/CroissantBot?sort=semver"></a>
    <a href="//github.com/JulioLoayzaM/CroissantBot/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/JulioLoayzaM/CroissantBot?style=flat"></a>
</p>


> La documentación también está disponible en [Español](docs/es/).

CroissantBot is a Discord bot written in Python using the [`discord.py` rewrite](https://github.com/Rapptz/discord.py).

While the bot itself is not openly available, its code is.
This repo aims to be a template to ease the creation of a new bot, allowing anyone\* to clone it, fill in the blanks with [its documentation](docs/) and run it on their machine.

*some Python experience is recommended.

## Important info

The development of `discord.py` [has ended](https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1), in part due to the new `Message.content` privileged intent.
According to [this Discord dev post](https://support-dev.discord.com/hc/en-us/articles/4404772028055-Message-Content-Access-Deprecation-for-Verified-Bots), this new privileged intent (a permission to read messages, manually granted by Discord) should not be a problem for "Unverified bots in fewer than 100 servers".

Still, any change to the API won't be reflected in `discord.py`, so I'm currently waiting for the dust to settle to see if/when a viable fork emerges.
For now, I'll continue working on this bot as if nothing happened.

## Features

> For a list of all commands, [check the docs](docs/commands.md).

#### Music player

Play music from YouTube in voice chat. Supports playback on different servers simultaneously, with a queue for each one.

#### Memes

Get memes from Reddit. Keeps track of memes sent to each server to avoid duplicates.

#### Kill messages

Sends a message targeting a specified server member. Keeps count of kills in each server. Messages not included.

#### Livestream status

Sometimes Twitch's notifications are unreliable, so the bot can notify users about new streams through DMs. It works with YouTube streams as well. **This feature can be disabled.**

#### Logging

Outputs basic information and errors to `stdout`. Debug information is logged to a file. It should allow to at least pinpoint which function has caused an error.

## How to run

Most commands depend on a *cog*, an extension used to group commands. For example, all music commands belong to the [Music cog](cogs/music.py).

The bot uses a `.env` file. This allows to put all credentials in one place, instead of placing them in the source code, and allows to easily turn on and off some features.

For example, the `twitch` and `youtube` cogs can be disabled ([see below](README.md#disabling-cogspartial-installation)). *It is recommended to do so* if you are not planning to use them, in order to avoid setting them up. You can enable them later on.

The **bot's default prefix** is `!`. You can change it in `.env`.

### Dependencies

I've tested the bot with `Python 3.6.9` in Ubuntu 18.04 and `Python 3.6.1` in Windows 10 using the following packages:

| Package             | Usage                                                        | Tested version |
| ------------------- | ------------------------------------------------------------ | -------------- |
| `discord.py[voice]` | API wrapper for Discord with voice support                   | `1.7.3`        |
| `python-dotenv`     | To store API keys and other secrets in a `.env` file         | `0.18.0`       |
| `youtube-dl`        | To get music from YouTube                                    | `2021.6.6`     |
| `asyncpraw`         | Asynchronous Python Reddit API Wrapper, to get memes from Reddit | `7.3.0`        |
| `streamlink`        | To check for YouTube livestreams                             | `2.3.0`        |
| `packaging`         | To check the bot's current version                           | `20.9`         |

### Full installation

- If you have a GitHub account, [clone the repo](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository).
  - If not, create one or check [the releases page](https://github.com/JulioLoayzaM/CroissantBot/releases) to get the latest one.

  > Cloning the repo is recommended in order to use Git to easily update the bot.

- Install Python 3.6+: use your package manager or head over to [the download page](https://www.python.org/downloads/).

  > This should install `pip`, Python's package installer. If unsure, read [`pip`'s getting started](https://pip.pypa.io/en/stable/getting-started/) to verify and install it if needed.

- Optional but recommended: create a [virtual environment](https://python.land/virtual-environments/virtualenv) to avoid conflicts with the dependencies.

- Install the package dependencies with `pip install -U -r requirements.txt`.

- Create the bot on Discord's side and get its token with [this doc](docs/bot.md).

- Get the necessary credentials for the required cogs: [meme](docs/meme.md), [misc](docs/misc.md) and [music](docs/music.md).

  - If enabled, get the credentials for the optional cogs: [twitch](docs/twitch.md) and/or [youtube](docs/youtube.md). If using the `music` cog, install `FFmpeg` using a package manager or through its [the download page](https://www.ffmpeg.org/download.html).

- Use them to fill [`.env.example`](.env.example).

- Rename the file to `.env`.

- Add the bot to a server: for instructions return to [this doc](docs/bot.md).

- Then, run `bot.py`:

  - Linux/macOS:

    ```
    python3 bot.py
    ```

  - Windows:

    ```
    python bot.py
    ```

### Disabling cogs/partial installation

The `twitch` and `youtube` cogs are optional. They are used to notify users of new streams in those platforms (the [livestream status](README.md#livestream-status) feature).

To disable them, set the `ENABLE_TW` and `ENABLE_YT` variables in `.env` to an empty string `""` or comment them, respectively.

Disabling a cog means its `.env` variables are not required:

- In the case of the `twitch` cog, it allows to skip the setup needed to use the Twitch API.
- As for the `youtube` cog, disabling it means its dependency `streamlink` is not required.

> Despite the name, it's the `music` cog and not the `youtube` one that uses `youtube-dl`, so don't forget to install it!

### Keeping the bot online

In order to continuously run the bot on my Raspberry Pi 4 I use [`tmux`](https://github.com/tmux/tmux/wiki).
It can create a detachable session which keeps the program running in the background, letting the user interact normally with the shell.
A `tmux` session can be reattached to the same or a different terminal or `ssh` session.

### Modifying the code

The idea of this template is to allow any modification to the code.
As such, and as stated [further down](README.md#license), the code can be freely modified under one condition: the content of the LICENSE file must be included with all copies or substantial portions of the code.
For more information, see the LICENSE file.
For an example on how this works, see the [music cog](cogs/music.py), which has code from [the basic_voice example](https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py) of `discord.py`.

## To-do

- [ ] One command for music - fuse play/play_from
- [x] Rotate the log files
- [ ] Switch from `youtube-dl` to `yt-dlp`
- [ ] Get the stream's thumbnail with `ytdl(p)`
- [x] Move from `requests` to `aiohttp`
- [ ] Test music streaming instead of downloading
- [ ] Auto-connect to channel when using `play`

## Considering

- [ ] Translation of docs to French
- [ ] Moderation commands
- [ ] Colour-coding embeds
- [ ] Way to disable other cogs
- [ ] Make this repo a template?
- [ ] Remove `members` intent
- [ ] Add support for slash commands
- [ ] Cache-clearing scripts examples

## Origin

I couldn't find the original video, but this meme is the inspiration for the name and `croissant` command: https://www.youtube.com/watch?v=s8VJ4QuVDBE.

## License

This project is available under the MIT license. See the [LICENSE.md](LICENSE.md) file for more info.

## Contributing

Feedback is welcome: share suggestions, feature ideas and bug reports by [opening an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue). Have a question? You can open an issue for that too.

Code contributions are also welcome, just fork the repo and [create a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests).

## Versioning

The versions of this repo follow the rules of [Semantic Versioning 2.0.0](https://semver.org/).
