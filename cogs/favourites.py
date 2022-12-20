# CroissantBot/cogs/favourites.py

"""
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

import aiofiles
import json
import os

from typing import List, Dict, Union

import discord
from discord.ext import commands

from cogs.music import YTDLSource, MaxDurationError


# Detect whether the music cog is enabled. If not, some commands are unavailable.
MUSIC_ENABLED = os.getenv("ENABLE_MUSIC")


class Favourites(commands.Cog):
    """Cog for managing the 'favourites' group of commands.

    These commands allow users of the bot to have one playlist, which is
    stored in a JSON file instead of using the Playlist cog that requires the use of a
    PostgreSQL database.
    """

    def __init__(self, bot: commands.Bot, ffile: str, max_duration: int):

        self.bot = bot
        self.logger = bot.logger
        self.flist: Union[Dict, None] = None
        self.ffile = ffile
        self.prefix = bot._prefix
        self.max_duration = max_duration

    @commands.group(
        name="favourites",
        aliases=["fav", "favorites"],
        help="Base command for managing your list of favourite songs",
    )
    async def favourites(self, ctx: commands.Context):
        """Base command for managing favourite songs.

        Loads the list of favourites from FAV_LIST_FILE during the first call.
        """

        # First verify a subcommand has been used.
        if ctx.invoked_subcommand is None:
            await ctx.send("You have to use a subcommand:")
            await ctx.send_help(self.favourites)
            return

        FAV_LIST_FILE = self.ffile
        logger = self.logger

        # TODO: Separate the lists for each user?
        # Then load the lists if needed.
        if self.flist is None:

            try:
                async with aiofiles.open(FAV_LIST_FILE, "r") as file:
                    content = await file.read()

                self.flist = json.loads(content) if content else dict()

            except IOError as ioe:
                logger.warning(
                    f'Could not open "{FAV_LIST_FILE}", maybe the file doesn\'t exist: ignoring.'
                )
                logger.debug(f"IOError:\n{ioe}")
                self.flist = dict()

            except Exception as e:
                logger.error(f'Could not load "{FAV_LIST_FILE}".')
                logger.debug(f"Unexpected exception:\n{e}")
                await ctx.send(
                    "A problem occurred while loading your list, please try again."
                )
                return

    @favourites.command(
        name="list",
        help="Displays your list of favourites songs: if an index is specified, shows that song's info",  # noqa: E501
    )
    async def fav_list(self, ctx: commands.Context, index: int = 0):
        """Subcommand to display the list of an user's favourite songs.

        Parameters:
                index: If less than or equal to zero, it displays the whole list.
                If greater than zero, it displays the song with that index in the list with more info.
        """

        FAV_LIST = self.flist

        member: discord.Member = ctx.message.author
        member_id: str = str(member.id)

        songs = FAV_LIST.get(member_id, None)

        if songs is not None:

            name = member.display_name
            # don't append an s if the last letter of the name is s
            title = f"{name}' list" if (name[-1] == "s") else f"{name}'s list"

            if len(songs) == 0:
                em = discord.Embed(title=title, description="Your list is empty.")
                await ctx.send(embed=em)
                return

            if index <= 0:

                cpt = 1
                message = ""
                for song in songs:
                    message += f"{cpt}. {song.get('title')}\n"
                    cpt += 1

                em = discord.Embed(
                    title=title, description=message, colour=member.colour
                )

                await ctx.send(embed=em)

            else:

                if index > len(songs):

                    await ctx.send(
                        f"There's no song with that index! Your list has {len(songs)} songs."
                    )

                else:

                    song = songs[index - 1]

                    em = discord.Embed(title=title, colour=member.colour)
                    em.add_field(name="Title", value=song.get("title"), inline=False)
                    em.add_field(name="URL", value=song.get("url"))
                    em.set_thumbnail(url=song.get("thumbnail"))

                    await ctx.send(embed=em)

        else:
            await ctx.send(
                f"You haven't saved any songs yet, use `{self.prefix}favourites add <song URL>` or "
                f"`{self.prefix}favourites now` to add one."
            )

    @favourites.command(name="add", help="Saves a song to your list from its URL")
    async def fav_add(self, ctx: commands.Context, url: str = ""):
        """Saves a song to the user's list: uses from_url to get the title
        and the thumbnail's URL.

        Parameters:
                url: The URL of the song to save.
        """

        if len(url) == 0:
            await ctx.send("You have to provide a URL.")
            return

        FAV_LIST_FILE = self.ffile
        logger = self.logger

        try:
            # Suppress the embed to avoid clutter.
            msg: discord.Message = ctx.message
            await msg.edit(suppress=True)

            song = await YTDLSource.from_url(url, self.max_duration, download=False)
            info = dict()
            info["title"] = song.title
            info["url"] = song.url
            info["thumbnail"] = song.thumbnail

            member: discord.Member = ctx.message.author
            member_id: str = str(member.id)

            songs = self.flist.get(member_id, None)

            if songs is not None:
                songs.append(info)
            else:
                songs = [info]
                self.flist[member_id] = songs

            dump = json.dumps(self.flist)
            async with aiofiles.open(FAV_LIST_FILE, "w") as file:
                await file.write(dump)

            em = discord.Embed(
                description=f"Added \"{info.get('title')}\" to your list.",
                colour=member.colour,
            )

            await ctx.send(embed=em)

        except MaxDurationError:
            await ctx.send("The song is too long to be played, so it can't be saved.")

        except Exception as e:
            logger.error("Could not add a song to list of favourites.")
            logger.debug(f"Exception:\n{e}")
            await ctx.send("An error occurred while saving the song, please try again.")

    @favourites.command(
        name="remove",
        help="Removes a song from your list by its index, 0 means no song is removed",
    )
    async def fav_remove(self, ctx: commands.Context, index: int = 0):
        """Remove a song from the user's list by its index.

        Parameters:
                index: The index of the song to remove, 0 by default to avoid removing anything.
        """

        if index <= 0:
            await ctx.send(
                "You have to provide a valid index."
                f"Use `{self.prefix}favourites list` to check your list."
            )
            return

        FAV_LIST_FILE = self.ffile
        logger = self.logger

        member_id: str = str(ctx.message.author.id)
        songs: List[Dict[str, str]] = self.flist.get(member_id, None)

        if songs is None:
            await ctx.send("You haven't saved any songs yet.")
            return

        if index > len(songs):
            await ctx.send(
                f"You have to select a valid index: there's only {len(songs)} songs in your list."
            )
            return

        song = songs.pop(index - 1)

        try:
            dump = json.dumps(self.flist)
            async with aiofiles.open(FAV_LIST_FILE, "w") as file:
                await file.write(dump)

            message = f"Removed \"{song.get('title')}\" from your list."
            em = discord.Embed(description=message)
            await ctx.send(embed=em)

        except Exception as e:
            logger.error("Couldn't save favourites list after removing a song.")
            logger.debug(f"Exception:\n{e}")

    @favourites.command(
        name="now",
        help="Saves the currently playing song to your list",
        enabled=MUSIC_ENABLED,
        hidden=not MUSIC_ENABLED,
    )
    @commands.guild_only()
    async def fav_now(self, ctx: commands.Context):
        """Saves the currently playing song from self.info.source."""

        music = self.bot.get_cog("Music")
        gid = ctx.message.guild.id

        if gid not in music.info:
            await ctx.send("The bot is not connected to a voice channel.")
            return

        BOT_PREFIX = self.prefix
        FAV_LIST_FILE = self.ffile
        logger = self.logger

        info = music.info.get(gid)
        source: YTDLSource = info.get("source")

        if source is not None:

            member_id: str = str(ctx.message.author.id)

            songs = self.flist.get(member_id, None)

            song = dict()
            song["title"] = source.title
            song["url"] = source.url
            song["thumbnail"] = source.thumbnail

            if songs is not None:
                songs.append(song)
            else:
                songs = [song]
                self.flist[member_id] = songs

            try:
                dump = json.dumps(self.flist)
                async with aiofiles.open(FAV_LIST_FILE, "w") as file:
                    await file.write(dump)

                em = discord.Embed(
                    description=f"Added \"{song.get('title')}\"to your list."
                )

                await ctx.send(embed=em)

            except Exception as e:
                logger.error("Could not save a song to FAV_LIST_FILE.")
                logger.debug(f"Exception:\n{e}")
                await ctx.send(
                    "An error occurred while saving the song, please try again."
                )

        else:

            await ctx.send(
                f"The bot is not playing something at the moment, try `{BOT_PREFIX}play <song>`."
            )

    @favourites.command(
        name="play",
        help="Plays a song from your list by its index",
        enabled=MUSIC_ENABLED,
        hidden=not MUSIC_ENABLED,
    )
    @commands.guild_only()
    async def fav_play(self, ctx: commands.Context, index: int = 0):
        """
        Play a song from the user's list by passing its URL to self.play.

        Parameters:
                index: The index of the song to play, 0 by default.
        """

        if index <= 0:
            await ctx.send("You have to provide a valid index.")
            return

        BOT_PREFIX = self.prefix
        FAV_LIST = self.flist

        member_id: str = str(ctx.message.author.id)
        songs = FAV_LIST.get(member_id, None)

        if songs is None:
            await ctx.send(
                f"You haven't saved a song yet, you can use `{BOT_PREFIX}favourites add <URL>` "
                f"or `{BOT_PREFIX}favourites now`."
            )
            return

        if index > len(songs):
            await ctx.send(
                f"You have to provide a valid index, your list only has {len(songs)} songs."
            )
            return

        song = songs[index - 1]
        url = song.get("url")
        music = self.bot.get_cog("Music")
        await music.play(ctx, url)


async def setup(bot):

    # Name of the file in which the list of favourites is kept.
    # By default it's 'favourite_songs.json', the directory is rsc/
    fav_list_file = os.getenv("MUSIC_FAV_LIST")
    max_duration = int(os.getenv("MAX_DURATION"))

    await bot.add_cog(Favourites(bot, fav_list_file, max_duration))
