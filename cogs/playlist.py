# CroissantBot/cogs/playlist.py

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

import os
import yt_dlp

import discord
from discord.ext import commands

from cogs.ext.music_db import MusicDatabaseConnection
from cogs.ext.db import DbInsertError, NotFoundError
from cogs.music import YTDLSource


MUSIC_ENABLED = bool(os.getenv("ENABLE_MUSIC", False))

DB_CONNECTED = False


def check_if_db_is_connected():
    """
    Custom check to verify that the bot is connected to the database.
    This prevents the subcommands from running if the connection failed.
    """

    def predicate(ctx: commands.Context):
        return DB_CONNECTED

    return commands.check(predicate)


class Playlist(commands.Cog):
    """
    Commands to manage playlists.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = MusicDatabaseConnection("CroissantBot")
        self.logger = bot.logger

    async def close_db(self) -> bool:
        """
        Closes the connection to the database.

        Returns:
                True if the database was closed, False otherwise.
        """

        return await self.db.close()

    async def is_connected_to_vc(self, ctx: commands.Context):
        """
        Checks if the bot is connected to a voice channel.

        :return:
                True if connected, False otherwise.
        :rtype: bool
        """
        music = self.bot.get_cog("Music")
        if music is None:
            return False
        return await music.is_connected(ctx)

    @commands.group(
        name="playlist", aliases=["pl"], help="Base command for managing your playlists"
    )
    async def playlist_base(self, ctx: commands.Context):
        """
        Base function for playlist management.
        """
        global DB_CONNECTED

        if ctx.invoked_subcommand is None:
            await ctx.send("You have to use a subcommand:")
            await ctx.send_help(self.playlist_base)
            return

        if not await self.db.is_connected():
            host = os.getenv("DB_MUSIC_HOST")
            user = os.getenv("DB_MUSIC_USER")
            port = os.getenv("DB_MUSIC_PORT", None)
            password = os.getenv("DB_MUSIC_PASSWORD")
            database = os.getenv("DB_MUSIC_DATABASE")

            try:
                await self.db.connect(
                    host, user, password, database, self.bot.loop, port
                )
                DB_CONNECTED = True
            except Exception as error:
                message, *rest = error.args
                self.logger.error(message)
                self.logger.debug(rest)
                await ctx.send(
                    "An error occurred while getting the playlists,"
                    " please contact the bot's admin."
                )

    @playlist_base.command(name="add", help="Adds a song to a playlist")
    @check_if_db_is_connected()
    async def playlist_add(
        self, ctx: commands.Context, song_url: str, list_title: str = "favourites"
    ):
        """
        Adds a song from its URL to a playlist. Creates the playlist if it doesn't exist.

        Parameters:
                song_url: The song's URL.
                list_title: The title of the playlist. 'favourites' by default,
                to quickly save songs.
        """

        if not await validate_url(song_url):
            await ctx.send("You have to use a valid URL.")
            return

        # To avoid clutter, we edit the message to remove the embed.
        await ctx.message.edit(suppress=True)

        song = await YTDLSource.from_url(
            song_url,
            max_duration=int(os.getenv("MAX_DURATION")),
            loop=self.bot.loop,
            download=False,
        )

        try:
            added, created = await self.db.add_song_to_playlist(
                song, list_title, str(ctx.author.id)
            )
            # first send an embed if the playlist was created by this action
            if created:
                em = discord.Embed(
                    title="Created playlist",
                    description=list_title,
                    colour=discord.Colour.green(),
                )
                await ctx.send(embed=em)
            # then send one indicating whether the song was added to the playlist
            if added:
                em = discord.Embed(
                    title=f"Added to {list_title}",
                    description=song.title,
                    colour=discord.Colour.green(),
                )
            else:
                em = discord.Embed(
                    title="Song already in playlist",
                    description=f"{song.title} is already in {list_title}",
                    colour=discord.Colour.gold(),
                )
            await ctx.send(embed=em)
        except DbInsertError as error:
            message, *_ = error.args
            em = discord.Embed(
                title="Error", description=message, colour=discord.Colour.red()
            )

    @playlist_base.command(
        name="remove", help="Remove a song from a playlist by its index"
    )
    @check_if_db_is_connected()
    async def playlist_remove(self, ctx: commands.Context, title: str, index: int):
        """
        Removes a song from a playlist by its index.

        Parameters:
                title: The title of the playlist.
                index: The index of the song to remove.
        """

        if not await self.db.playlist_exists(title, str(ctx.author.id)):
            em = discord.Embed(
                title="Error",
                description=f"""You don't have a playlist named {title}.\n
				Use `{self.bot._prefix}playlist create <title>` to create a playlist.""",
                colour=discord.Colour.gold(),
            )
            await ctx.send(embed=em)
            return

        try:
            await self.db.remove_song_from(title, str(ctx.author.id), index)
        except NotFoundError as error:
            message, *_ = error.args
            em = discord.Embed(
                title="Error", description=message, colour=discord.Colour.gold()
            )
            await ctx.send(embed=em)
        except DbInsertError as error:
            message, *rest = error.args
            em = discord.Embed(
                title="Error", description=message, colour=discord.Colour.gold()
            )
            await ctx.send(embed=em)
            self.logger.error("Could not remove song from playlist.")
            self.logger.debut(rest)

    @playlist_base.command(
        name="now",
        help="Adds the currently playing song to a playlist, favourites by default",
        enabled=MUSIC_ENABLED,
        hidden=not MUSIC_ENABLED,
    )
    @check_if_db_is_connected()
    async def playlist_now(self, ctx: commands.Context, title: str = "favourites"):
        """
        Adds the currently playing or paused song to a user's playlist.

        Parameters:
                title: The title of the playlist to add the song to, favourites by default.
        """

        music = self.bot.get_cog("Music")
        if music is None:
            em = discord.Embed(
                title="Error",
                description="An error occurred while loading the playlists.",
                colour=discord.Colour.red(),
            )
            await ctx.send(embed=em)
            return

        if not await music.is_connected(ctx):
            em = discord.Embed(
                title="Error",
                description="The bot is not connected to a voice channel",
                colour=discord.Colour.gold(),
            )
            await ctx.send(embed=em)
            return

        gid = ctx.message.guild.id
        info = music.info.get(gid)
        source: YTDLSource = info.get("source")

        if source is not None:
            song_url = source.url
            await self.playlist_add(ctx, song_url, str(ctx.author.id), title)
        else:
            em = discord.Embed(
                title="Error",
                description="The bot is not playing something.",
                colour=discord.Colour.gold(),
            )
            await ctx.send(embed=em)

    @playlist_base.command(name="create", help="Creates a new playlist")
    @check_if_db_is_connected()
    async def playlist_create(self, ctx: commands.Context, title: str):
        """
        Creates a new playlist if no other playlist owned by the user has the same title.

        Parameters:
                title: The title to give to the playlist.
        """

        try:
            await self.db.create_playlist(title, str(ctx.author.id))
            em = discord.Embed(
                title="Created playlist",
                description=title,
                colour=discord.Colour.green(),
            )
            await ctx.send(embed=em)
        except DbInsertError as error:
            message, *rest = error.args
            em = discord.Embed(
                title="Error", description=message, colour=discord.Colour.red()
            )
            await ctx.send(embed=em)
            self.logger.debug(f"DbInsertError: {rest}")

    @playlist_base.command(name="delete", help="Deletes a playlist")
    @check_if_db_is_connected()
    async def playlist_delete(self, ctx: commands.Context, title: str):
        """
        Deletes a playlist from the database, if it exists.

        Parameters:
                title: The title of the playlist to delete.
        """

        try:
            await self.db.delete_playlist(title, str(ctx.author.id))
            em = discord.Embed(
                title="Deleted", description=title, colour=discord.Colour.green()
            )
            await ctx.send(embed=em)
        except DbInsertError as error:
            message, *rest = error.args
            em = discord.Embed(
                title="Error", description=message, colour=discord.Colour.red()
            )
            await ctx.send(embed=em)
            self.logger.error("Error deleting a playlist.")
            self.logger.debug(rest)

    @playlist_base.command(
        name="list",
        help="Lists all your playlists by default or shows the songs in a specific one",
    )
    @check_if_db_is_connected()
    async def playlist_list(self, ctx: commands.Context, title: str = None):
        """
        Show the user's playlists or songs in a specific playlist.

        Parameters:
                title: The title of the playlist to display. If None, displays a list of
                all the user's playlists. None by default.
        """

        if title is None:
            playlists = await self.db.get_playlists(str(ctx.author.id))
            if playlists is None:
                await ctx.send(
                    "You haven't created a playlist yet, use"
                    f" `{self.bot._prefix}playlist create <title>` to create one."
                )
            else:
                cpt = 1
                msg = ""
                for pl in playlists:
                    msg += f"{cpt}. {pl}\n"
                    cpt += 1
                name = ctx.author.display_name
                if name[-1].lower == "s":
                    em_title = f"{name}' playlists"
                else:
                    em_title = f"{name}'s playlists"
                em = discord.Embed(
                    title=em_title, description=msg, colour=ctx.author.colour
                )
                await ctx.send(embed=em)

        else:
            songs = await self.db.get_titles_in_playlist(title, str(ctx.author.id))
            if songs is None:
                await ctx.send(
                    "You haven't saved songs to this playlist,"
                    f" use `{self.bot._prefix}playlist add <song URL> <playlist title>`."
                )
            else:
                cpt = 1
                msg = ""
                for song in songs:
                    msg += f"{cpt}. {song}\n"
                    cpt += 1
                em = discord.Embed(
                    title=title, description=msg, colour=ctx.author.colour
                )
                await ctx.send(embed=em)

    @playlist_base.command(
        name="play",
        help="Adds a playlist to the queue, or a specific song from a playlist",
        enabled=MUSIC_ENABLED,
        hidden=not MUSIC_ENABLED,
    )
    @check_if_db_is_connected()
    async def playlist_play(
        self, ctx: commands.Context, title: str = "favourites", index: int = 0
    ):
        """
        Queues all songs from a playlist, or a specific song from a playlist.

        Parameters:
                title: The title of the playlist to queue or to get the song from.
                'favourites' by default.
                index: The index of the song to queue. If 0, queues all the songs in
                the playlist. If the index exists in the playlist, queues that specific song.
        """

        if not await self.is_connected_to_vc(ctx):
            em = discord.Embed(
                title="Error",
                description="The bot is not connected to a voice channel.",
                colour=discord.Colour.gold(),
            )
            await ctx.send(embed=em)
            return

        if not await self.db.playlist_exists(title, str(ctx.author.id)):
            em = discord.Embed(
                title="Error",
                description=f"""You don't have a playlist named {title}.\n
				Use `{self.bot._prefix}playlist create <title>` to create a playlist.""",
                colour=discord.Colour.gold(),
            )
            await ctx.send(embed=em)
            return

        if index == 0:
            songs = await self.db.get_songs_in_playlist(title, str(ctx.author.id))
            if songs is None:
                em = discord.Embed(
                    title="Error",
                    description=f"""You don't have songs saved in {title}.\n
					Use `{self.bot._prefix}playlist add <song_url> {title}` to add a song.""",
                    colour=discord.Colour.gold(),
                )
                await ctx.send(embed=em)
            else:
                music = self.bot.get_cog("Music")
                if music is None:
                    em = discord.Embed(
                        title="Error",
                        description="An error occurred while loading the playlists.",
                        colour=discord.Colour.red(),
                    )
                    await ctx.send(embed=em)
                    return
                for song in songs:
                    await music.play(ctx, song)
        elif index < 0:
            em = discord.Embed(
                title="Error",
                description="You can't use a negative index!",
                colour=discord.Colour.gold(),
            )
            await ctx.send(embed=em)
        else:
            song = await self.db.get_song_from(index, title, str(ctx.author.id))
            if song is None:
                em = discord.Embed(
                    title="Error",
                    description=f"There's no song with that index in {title}.",
                    colour=discord.Colour.gold(),
                )
                await ctx.send(embed=em)
            else:
                music = self.bot.get_cog("Music")
                if music is None:
                    em = discord.Embed(
                        title="Error",
                        description="An error occurred while loading the playlists.",
                        colour=discord.Colour.red(),
                    )
                    await ctx.send(embed=em)
                    return
                await music.play(ctx, song)


async def validate_url(url: str) -> bool:
    """
    Checks to see if url has any valid extractors for yt_dlp.

    Parameters:
            url: The url to search for extractors.

    Returns:
            True if site has dedicated extractor, False otherwise.
    """
    e = yt_dlp.extractor.get_info_extractor("Youtube")
    return e.suitable(url)


async def setup(bot):

    await bot.add_cog(Playlist(bot))
