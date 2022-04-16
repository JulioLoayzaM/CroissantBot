# CroissantBot/cogs/base.py

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

import asyncio
import logging

from packaging import version
from random import randint

from discord import Colour, Embed
from discord.ext import commands

from bot import CroissantBot

GREEN   = '\033[92m'
WARNING = '\033[93m'
BLUE    = '\033[94m'
ENDC    = '\033[0m'
VOICE = f"{BLUE}[voice]{ENDC}"


class Base(commands.Cog):
    """Cog for the base commands.

    This cog contains the basic, necessary commands:
      - exit
      - ping
      - reload
      - version
    """

    def __init__(self, bot: CroissantBot):
        """"""
        self.bot = bot

    @commands.command(
        name="exit",
        help="Closes the bot"
    )
    @commands.is_owner()
    async def close_connection(self, ctx: commands.Context):
        """Closes the bot's connection.

        Cleans the voice clients, the requests session and logging.
        Checks if the cogs are enabled, since failing to get the cog is not an error
        if they are not enabled.
        """

        bot = self.bot
        logger = bot.logger

        # Close all voice clients
        if 'MUSIC' in bot.enabled_cogs:
            music = bot.get_cog('Music')
            if music is not None:
                if await music.stop_all():
                    logger.debug(f"{VOICE} stop_all executed.")
            else:
                logger.error("Couldn't get cog 'Music'.")

        # Close connection to the database.
        if 'PLAYLIST' in bot.enabled_cogs:
            pl = bot.get_cog('Playlist')
            if pl is not None:
                if await pl.close_db():
                    logger.debug(f"{GREEN}Disconnected from database.{ENDC}")
                else:
                    logger.debug(f"{WARNING}The database was already closed.{ENDC}")
            else:
                logger.error("Couldn't get cog 'Playlist'")

        # Close the reddit session.
        if 'MEME' in bot.enabled_cogs:
            meme = bot.get_cog('Meme')
            if meme is not None:
                if await meme.close_session():
                    logger.debug(
                        f"{WARNING}Closed:{ENDC} Reddit instance."
                    )
            else:
                logger.error("Couldn't get cog 'Meme'.")

        # Close the global aiohttp.ClientSession
        await bot._session.close()
        logger.debug(f"{WARNING}Closed:{ENDC} Global aiohttp.ClientSession.")

        em = Embed(
            description="I'm leaving!",
            colour=Colour.green()
        )
        await ctx.send(embed=em)
        # Close the bot
        await bot.close()
        logger.info(f"{GREEN}Bot offline.{ENDC}")

        logging.shutdown()

    @commands.command(
        name="ping",
        help="Pings the bot, shows its current latency"
    )
    async def ping_back(self, ctx: commands.Context):
        """
        Simple ping command. Has a mini easter egg.
        If the bot is connected to a voice channel, sends the current and average latency.
        """

        bot = self.bot

        # Mini easter egg
        r = randint(1, 3)
        name = "Latency:ping_pong:" if r == 1 else "Latency"

        em = Embed()
        em.add_field(
            name=name,
            value=f"{round(bot.latency * 1000)} ms",
            inline=False
        )

        music = bot.get_cog('Music')

        if (bot.cogs.get('MUSIC', False)) and (music is not None):
            res = await music.get_latency(ctx)
            if res is not None:
                latency, average = res
                if latency != float('inf'):
                    em.add_field(
                        name="Voice latency",
                        value=f"{round(latency * 1000)} ms"
                    )
                if average != float('inf'):
                    em.add_field(
                        name="Voice average latency",
                        value=f"{round(average * 1000)} ms"
                    )
        await ctx.send(embed=em)

    @commands.command(
        name="reload",
        help="Reloads a cog"
    )
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, name: str):
        """
        Reloads a cog. Useful for testing changes without restarting the bot.

        Parameters:
            name: The name of the cog to reload.
        """

        bot = self.bot
        logger = bot.logger

        if not name.startswith("cogs."):
            name = "cogs." + name
        try:
            bot.reload_extension(name)
        except commands.ExtensionNotLoaded as error:
            await ctx.send("That cog is not loaded.")
            logger.debug(error)
        except commands.ExtensionNotFound as error:
            await ctx.send("Couldn't find that cog.")
            logger.debug(error)
        except commands.ExtensionFailed as error:
            await ctx.send("An error occurred while reloading the cog, \
                reverting to last working state.")
            logger.error("The extension setup function had an execution error.")
            logger.debug(error)
        except Exception as error:
            await ctx.send("An error occurred while reloading the cog, \
                reverting to last working state.")
            logger.debug(error)

    @commands.command(
        name="version",
        help="Get the bot's current version, use option 'remote' to check the latest version",  # noqa: 501
        aliases=['ver']
    )
    @commands.is_owner()
    async def check_version(self, ctx: commands.Context, option: str = "local"):
        """
        Checks the current bot version.
        Can check the latest release on GitHub.	If the bot's not up to date,
        it shows what type of update (major|minor|patch) is available, the
        corresponding release message, and a link to the releases page.
        Can also get the full release notes with 'notes' option.

        Parameters:
            option:
                'local': to check only the bot's current version,
                'remote': to check the current version and the repo's latest version,
                'notes': to get the full release notes.
                Default: 'local'.
        """

        bot = self.bot
        logger = bot.logger

        # Get the local version: uses Git to check the latest (annotated) tag,
        # so it's not possible to get local version if the repo wasn't cloned.
        try:
            proc = await asyncio.create_subprocess_shell(
                'git describe --abbrev=0',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()

            if stdout:
                output = stdout.decode('utf-8').rstrip()
            else:
                raise Exception(f"stdout is empty: {stdout}\nstderr: {stderr}")

            local_ver = version.parse(output)

        except Exception as e:
            logger.warning("Error getting current bot version, ignoring.")
            logger.debug(f"Error:\n{e}")
            local_ver = None

        if option == "local":

            if local_ver is None:
                await ctx.send("Could not get local version.")
                return

            else:
                em = Embed(
                    title=f"The bot's current version is {local_ver}",
                    description=f"Use `{bot._prefix}version remote` to check for updates."
                )
                await ctx.send(embed=em)

        elif option == "remote":

            # Get remote version
            remote_api_url = "https://api.github.com/repos/JulioLoayzaM/CroissantBot/releases/latest"  # noqa: 501
            header = {'Accept': "application/vnd.github.v3+json"}

            async with bot._session.get(remote_api_url, headers=header) as response:
                latest: dict = await response.json()

            remote_ver = version.parse(latest.get('tag_name'))

            # Determine the embed's colour first - the colour has to be set
            # during initialization, but that would mean creating the embed
            # and adding the version fields on every case.
            if local_ver is None:
                colour = Colour.red()
            else:
                if local_ver == remote_ver:
                    colour = Colour.green()
                elif local_ver < remote_ver:
                    colour = Colour.gold()
                else:
                    colour = Colour.teal()

            # Create the embed with the colour
            em = Embed(colour=colour)

            if local_ver is None:

                em.add_field(
                    name="Current version",
                    value="Could not get the current version",
                    inline=True
                )
                em.add_field(
                    name="Latest version",
                    value=f"{remote_ver}",
                    inline=True
                )
                em.add_field(
                    name="Changelog",
                    value="https://github.com/JulioLoayzaM/CroissantBot/releases",
                    inline=False
                )
                await ctx.send(embed=em)

            else:

                em.add_field(
                    name="Current version",
                    value=f"{local_ver}",
                    inline=True
                )
                em.add_field(
                    name="Latest version",
                    value=f"{remote_ver}",
                    inline=True
                )

                # MAYBE: add support for release candidates?
                if local_ver == remote_ver:
                    em.add_field(
                        name="Status",
                        value="Nothing to do, the bot's up to date!",
                        inline=False
                    )

                elif local_ver < remote_ver:

                    if local_ver.major < remote_ver.major:
                        status_message = "A new **major** version is available.\n"
                        status_message += "**Warning:** a major update may contain"
                        status_message += " breaking changes.\n"
                        status_message += "Please check the changelog first, then"
                        status_message += " use `git pull` to update."
                        em.add_field(name="Status", value=status_message, inline=False)

                    elif local_ver.minor < remote_ver.minor:
                        status_message = "A new **minor** version is available."
                        status_message += " Use `git pull` to update."
                        em.add_field(name="Status", value=status_message, inline=False)

                    else:
                        status_message = "A new **patch** is available."
                        status_message += " Use `git pull` to update."
                        em.add_field(name="Status", value=status_message, inline=False)

                    # Extract the message before the patch notes
                    body: str = latest.get('body')
                    # The notes start with an H2 header
                    index = body.index('##')
                    release_message = body[:index]
                    # The message should contain a couple of newlines at the end.
                    # Just in case, we get rid of them and add new ones.
                    release_message = release_message.rstrip('\r\n')
                    release_message += "\n\n"
                    release_message += "Read the release notes with "
                    release_message += f"`{bot._prefix}version notes` "
                    release_message += "or in the changelog below."

                    em.add_field(
                        name="Release message",
                        value=f"{release_message}",
                        inline=False
                    )

                    changelog_url = "https://github.com/JulioLoayzaM/CroissantBot/releases"  # noqa: 501
                    em.add_field(
                        name="Changelog",
                        value=changelog_url,
                        inline=False
                    )

                else:
                    status_message = "Your version is more recent than mine! "
                    status_message += "How'd you do that?\n"
                    status_message += "(If you believe this to be an error, "
                    status_message += "don't hesitate to report it in the repo below!)"
                    em.add_field(
                        name="Status",
                        value=status_message,
                        inline=False
                    )

                    em.add_field(
                        name="Repo",
                        value="https://github.com/JulioLoayzaM/CroissantBot",
                        inline=False
                    )

                await ctx.send(embed=em)

        elif option == 'notes':

            remote_api_url = "https://api.github.com/repos/JulioLoayzaM/CroissantBot/releases/latest"  # noqa: 501
            header = {'Accept': "application/vnd.github.v3+json"}

            async with bot._session.get(remote_api_url, headers=header) as response:
                latest: dict = await response.json()

            remote_ver = version.parse(latest.get('tag_name'))

            title = f"CroissantBot version {remote_ver} release notes:"

            body = latest.get('body')

            em = Embed(title=title, description=body)

            changelog_url = "https://github.com/JulioLoayzaM/CroissantBot/releases"
            em.add_field(name="Changelog", value=changelog_url, inline=False)

            await ctx.send(embed=em)

        else:

            message = ""
            message += "- `local`: default, shows the bot's current version.\n"
            message += "- `remote`: shows the current and the latest version, \
                indicates if an update is available.\n"
            message += "- `notes`: shows the release notes of the latest version.\n"
            message += "- anything else: shows this help message."
            em = Embed(
                title="Version options",
                description=message
            )

            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Base(bot))
