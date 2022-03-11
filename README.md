# CroissantBot

<p align="center">
    <a href="//www.python.org/">
      <img src="https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54">
    </a>
    <a href="//github.com/JulioLoayzaM/CroissantBot/releases">
      <img src="https://img.shields.io/github/v/release/JulioLoayzaM/CroissantBot?sort=semver&style=flat">
    </a>
    <a href="//github.com/JulioLoayzaM/CroissantBot/blob/main/LICENSE.md">
      <img src="https://img.shields.io/github/license/JulioLoayzaM/CroissantBot?style=flat">
    </a>
    <a href='https://croissantbot.readthedocs.io/en/latest/?badge=latest'>
      <img src='https://readthedocs.org/projects/croissantbot/badge/?version=latest' alt='Documentation Status' />
    </a>
</p>

> Este README está disponible en [Español](docs/es/LEEME.md).

CroissantBot is a Discord bot written in Python using the [`discord.py` rewrite](https://github.com/Rapptz/discord.py).

It started as a personal replacement for Dankmemer and Groovy, and grew to something I wanted to share: while my instance is not openly available, the code is.
This repo aims to provide a template to help anyone\* create their own bot by just cloning the repo, fill in the blanks with [its documentation](https://croissantbot.readthedocs.io/en/latest/) and run it on their machine.

*some Python experience is recommended.

## Table of contents
- [The future of this bot](#the-future-of-this-bot)
- [Features](#features)
  - [Music player](#music-player)
  - [Playlists](#playlists)
  - [Memes](#memes)
  - [Kill messages](#kill-messages)
  - [Livestream status](#livestream-status)
  - [Logging](#logging)
- [How to run](#how-to-run)
- [Modifying the code](#modifying-the-code)
- [Origin](#origin)
- [License](#license)
- [Contributing](#contributing)
- [Versioning](#versioning)

## The future of this bot

The development of `discord.py` [ended a few months ago](https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1), due in part to the new `Message.content` privileged intent.

And then, [it resumed](https://gist.github.com/Rapptz/c4324f17a80c94776832430007ad40e6)!

I'll just say I am happy about Danny's return and thankful for the effort he and all the `discord.py` contributors made.
Simply put, it motivated me to continue developping this bot, even though I never intended to completely abandon it in the first place.

I think I'll mostly improve the existing code and upgrade it when possible to `discord.py` v2 so that my bot will continue working.
So far, it seems that the current code still does the job, although the transition to a new version will be necessary before May 1st,
as Discord is [shutting down v7 of their API](https://github.com/discord/discord-api-docs/discussions/4510),
which is what `discord.py`'s stable version (1.7.3) uses.

## Features

> For a list of all commands, [check the docs](https://croissantbot.readthedocs.io/en/latest/getting_started/commands.html).

### Music player

Play music from YouTube in voice chat, with support for playback on different servers simultaneously and a queue for each one.

### Playlists

Save as many playlists per user as you want with a PostgreSQL database and the Playlist cog. Or use the Favourites cog to save songs to a single playlist per user without using PostgreSQL.

### Memes

Get memes from Reddit and avoid duplicates by keeping track of memes sent to each server.

### Kill messages

Based on Dankmemer's feature, sends a message targeting a specified server member. It also keeps count of kills in each server. Messages are not included.

### Livestream status

Sometimes Twitch's notifications are unreliable, so the bot can notify users about new streams through DMs. It works with YouTube streams as well.

### Logging

Outputs basic information and errors to `stdout`. Debug information is logged to a file. It should allow to at least pinpoint which function has caused an error.

## How to run

The installation guide has been moved to [the documentation site](https://croissantbot.readthedocs.io/en/latest/).
An "offline" version can be found [here](docs/) and the old, incomplete version of the docs (pre-2.0.0) can be found [here](docs/v1).

## Modifying the code

The idea of this template is to allow any modification to the code.
As such, and as stated [further down](README.md#license), the code can be freely modified under one condition: the content of the LICENSE file must be included with all copies or substantial portions of the code.
For more information, see the LICENSE file.
For an example on how this works, see the [music cog](cogs/music.py), which has code from [the basic_voice example](https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py) of `discord.py`.

## Origin

I couldn't find the original video, but this meme is the inspiration for the name and `croissant` command: https://www.youtube.com/watch?v=s8VJ4QuVDBE.

## License

This project is available under the MIT license. See the [LICENSE.md](LICENSE.md) file for more info.

## Contributing

All contributions are welcome, see [CONTRIBUTING](.github/CONTRIBUTING.md).

## Versioning

The versions of this repo follow the rules of [Semantic Versioning 2.0.0](https://semver.org/).
