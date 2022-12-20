#!/usr/bin/env python
# CroissantBot/main.py

"""Main script.

Runs the bot:
	- sets up the loggers (CroissantBot, discord)
	- loads the base cog and any enabled cog
	- if enabled, starts the looping check functions
	- starts running the bot.


The MIT License (MIT)

Copyright (c) 2021-present JulioLoayzaM

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler

import discord

from bot import CroissantBot
from customformatter import CustomFormatter


GREEN = "\033[92m"
WARNING = "\033[93m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
ENDC = "\033[0m"


def setup_loggers() -> logging.Logger:
    """Sets up the loggers 'CroissantBot' and 'discord'.

    Handlers created:
            1: INFO-level to STDOUT
            2: INFO-level to a file
            3: DEBUG-level to a file
            4: discord DEBUG-level to a file

    Returns:
            The CroissantBot logger
    """

    log_dir = os.getenv("LOG_DIR")
    log_info = f'{log_dir}/{os.getenv("LOG_INFO")}'
    log_debug = f'{log_dir}/{os.getenv("LOG_DEBUG")}'
    log_discord = f'{log_dir}/{os.getenv("LOG_DISCORD")}'
    log_count = int(os.getenv("LOG_COUNT"))

    # Creates the CroissantBot logger
    logger = logging.getLogger("CroissantBot")
    logger.setLevel(logging.DEBUG)

    # Gets the discord logger
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.DEBUG)

    # Handler - writes INFO logging to stdout
    standard_handler = logging.StreamHandler()
    standard_handler.setLevel(logging.INFO)
    standard_handler.setFormatter(CustomFormatter())

    # Handler - writes INFO logging to file
    info_handler = TimedRotatingFileHandler(
        log_info, when="midnight", backupCount=log_count
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(CustomFormatter())

    # Handler - writes DEBUG logging to file
    debug_handler = TimedRotatingFileHandler(
        log_debug, when="midnight", backupCount=log_count
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(CustomFormatter())

    # Handler - writes DEBUG discord logging to file
    discord_debug_handler = TimedRotatingFileHandler(
        log_discord, when="midnight", backupCount=log_count
    )
    discord_debug_handler.setLevel(logging.DEBUG)
    discord_debug_handler.setFormatter(CustomFormatter())

    logger.addHandler(standard_handler)
    logger.addHandler(info_handler)
    logger.addHandler(debug_handler)

    discord_logger.addHandler(discord_debug_handler)

    logger.debug(f"{GREEN}Loggers set.{ENDC}")

    return logger


def setup_streamlink_logger():
    """Setup the streamlink logger.

    Fixes some annoyances caused by streamlink's logging, namely writing
    error messages to STDOUT and changing the levelnames to lowercase.
    """

    log_dir = os.getenv("LOG_DIR")
    log_streamlink = f'{log_dir}/{os.getenv("LOG_STREAMLINK")}'
    log_count = int(os.getenv("LOG_COUNT"))

    # Move streamlink logs to a file
    streamlink_handler = TimedRotatingFileHandler(
        log_streamlink, when="midnight", backupCount=log_count
    )
    streamlink_handler.setLevel(logging.DEBUG)
    logging.getLogger("streamlink").addHandler(streamlink_handler)

    # Restores the uppercase in levelnames
    logging.addLevelName(logging.DEBUG, "DEBUG")
    logging.addLevelName(logging.INFO, "INFO")
    logging.addLevelName(logging.WARNING, "WARNING")
    logging.addLevelName(logging.ERROR, "ERROR")
    logging.addLevelName(logging.CRITICAL, "CRITICAL")


async def load_cogs(bot: CroissantBot):
    """Load any enabled cogs.

    Load the cog and mark it as enabled.
    Start the check functions for the Twitch and Youtube cogs.
    """

    bot.logger.debug(f"{WARNING}Setting up bot...{ENDC}")

    await bot.load_extension("cogs.base")
    bot.enabled_cogs.append("BASE")

    if bool(os.getenv("ENABLE_JSONFAV", False)):
        await bot.load_extension("cogs.favourites")
        bot.enabled_cogs.append("FAVS")

    if bool(os.getenv("ENABLE_MEME", False)):
        await bot.load_extension("cogs.meme")
        bot.enabled_cogs.append("MEME")

    if bool(os.getenv("ENABLE_MISC", False)):
        await bot.load_extension("cogs.misc")
        bot.enabled_cogs.append("MISC")

    if bool(os.getenv("ENABLE_MUSIC", False)):
        await bot.load_extension("cogs.music")
        bot.enabled_cogs.append("MUSIC")

    if bool(os.getenv("ENABLE_PLAYLISTS", False)):
        await bot.load_extension("cogs.playlist")
        bot.enabled_cogs.append("PLAYLIST")

    if bool(os.getenv("ENABLE_TW", False)):
        await bot.load_extension("cogs.twitch")
        # https://discordpy.readthedocs.io/en/latest/ext/tasks/
        twitch_initiated = bot.loop.run_until_complete(bot.init_twitch())
        if twitch_initiated:
            bot._tw_task = await bot.loop.create_task(bot.check_twitch())
            bot.enabled_cogs.append("TWITCH")
        else:
            bot.logger.warning(
                f"Can't enable {PURPLE}twitch{ENDC} cog, unloading extension."
            )
            await bot.unload_extension("cogs.twitch")

    if bool(os.getenv("ENABLE_YT", False)):
        await bot.load_extension("cogs.youtube")
        youtube_initiated = bot.loop.run_until_complete(bot.init_youtube())
        setup_streamlink_logger()
        if youtube_initiated:
            bot._yt_task = bot.loop.create_task(bot.check_youtube())
            bot.enabled_cogs.append("YOUTUBE")
        else:
            bot.logger.warning(
                f"Can't enable {PURPLE}youtube{ENDC} cog, unloading extension."
            )
            await bot.unload_extension("cogs.youtube")

    bot.logger.debug(f"{WARNING}Enabled cogs:{ENDC} {bot.enabled_cogs}")


async def main():
    """Runs the bot.

    - Sets up the loggers
    - Loads any enabled cogs
    - If the twitch or youtube cogs are enabled, starts their corresponding check function;
    - Starts running the bot.
    """

    # pipenv automatically loads .env when using run or shell, so changes made
    # to .env aren't used unless override is set to True.
    # Another option is to use pipenv with PIPENV_DONT_LOAD_ENV, but I prefer
    # this solution for now.
    load_dotenv(".env", override=True)

    intents = discord.Intents.default()
    intents.members = True  # retrieve a guild's member list

    # This bot is intended for small servers that do not require bot verification,
    # so we can use the message_content intent. I'd still like to implement
    # slash commands, but that'll have to wait.
    intents.message_content = True

    prefix = os.getenv("BOT_PREFIX")
    logger = setup_loggers()
    bot = CroissantBot(prefix, intents, logger)

    token = os.getenv("BOT_TOKEN")

    await load_cogs(bot)

    logger.debug(f"{WARNING}Bot starting...{ENDC}")
    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
