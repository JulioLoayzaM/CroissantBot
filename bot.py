# bot.py - main file
#
# Runs the bot:
#	- sets up the loggers (CroissantBot, discord)
#	- loads the (selected) cogs
#	- if enabled, starts the looped functions
#	- starts running the bot.
# Includes some commands: exit, ping, test and version.


# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


import os
import random
import asyncio
import aiohttp
import logging
import json

from customformatter import CustomFormatter

import discord
from discord.ext import commands
from discord.ext.tasks import loop

from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv, set_key
from packaging import version


# .env variables
load_dotenv()

# Bot token
BOT_TOKEN = os.getenv('DISCORD_TOKEN')

# Bot prefix, '!' by default
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')

# Cog selection
TWITCH_ENABLED   = bool(os.getenv('ENABLE_TW', ''))
YOUTUBE_ENABLED  = bool(os.getenv('ENABLE_YT', ''))
PLAYLIST_ENABLED = bool(os.getenv('ENABLE_DB', ''))

# How often to check Twitch and/or Youtube, in minutes - 2 by default
if TWITCH_ENABLED or YOUTUBE_ENABLED:
	TW_FREQUENCY = int(os.getenv('TW_FREQUENCY', 2))
else:
	TW_FREQUENCY = 0

# Get the files of the enabled cogs
if TWITCH_ENABLED:
	TW_FILE = os.getenv('TW_FILE')
	TW_TOKEN = os.getenv('TW_TOKEN', '')
	TW_EXPIRES_IN = 0
if YOUTUBE_ENABLED:
	YT_FILE = os.getenv('YT_FILE')
	LOG_STREAMLINK_FILE = os.getenv('LOG_STREAMLINK')

# Log files
LOG_INFO_FILE    = os.getenv('LOG_INFO')
LOG_DEBUG_FILE   = os.getenv('LOG_DEBUG')
LOG_DISCORD_FILE = os.getenv('LOG_DISCORD')
LOG_COUNT = int(os.getenv('LOG_COUNT'))


# Colours for formatting console text
HEADER    = '\033[95m'
BLUE      = '\033[94m'
CYAN      = '\033[96m'
GREEN     = '\033[92m'
WARNING   = '\033[93m'
RED       = '\033[91m'
FAIL      = RED
ENDC      = '\033[0m'
BOLD      = '\033[1m'
UNDERLINE = '\033[4m'
PURPLE    = '\033[38;5;165m'

VOICE = f"{BLUE}[voice]{ENDC}"


# Create global variables for check_twitch/youtube
# Initialized by init_twitch/youtube
TW_PREV_STATUS = dict()
TW_STREAMERS   = dict()
YT_PREV_STATUS = dict()
YT_STREAMERS   = dict()

# Persistent session
SESSION: aiohttp.ClientSession = None

# Loggers
logger = None
discord_logger = None

# Discord intents
intents = discord.Intents.default()
# This one allows to retrieve a guild's member list
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


@bot.event
async def on_ready():
	"""
	Informs when the bot is connected, logs the guilds it's currently connected to.
	"""
	logger.info(f"{GREEN}{bot.user.name} online and connected to Discord.{ENDC}")
	guilds = ""
	for guild in bot.guilds:
		guilds += guild.name + ', '
	logger.debug(f"{GREEN}Connected to:{ENDC} {guilds[:-2]}.")


@bot.command(
	name="exit",
	help="Closes the bot, only usable by owner"
)
@commands.is_owner()
async def close_connection(ctx: commands.Context):
	"""
	Closes the bot's connection.
	Cleans the voice clients, the requests session and logging.
	"""

	# Close all voice clients
	res = False
	music = bot.get_cog('Music')
	if music is not None:
		res = await music.stop_all()
		if res:
			logger.debug(f"{VOICE} stop_all executed.")
	else:
		logger.error("Couldn't get cog 'Music'.")

	# Close connection to the database
	if PLAYLIST_ENABLED:
		res = False
		pl = bot.get_cog('Playlist')
		if pl is not None:
			res = await pl.close_db()
			if res:
				logger.debug(f"{GREEN}Disconnected from database.{ENDC}")
			else:
				logger.debug(f"{WARNING}The database was already closed.{ENDC}")

	# Close the meme aiohttp.ClientSession
	res = False
	meme = bot.get_cog('Meme')
	if meme is not None:
		res = await meme.close_session()
		if res:
			logger.debug(f"{WARNING}Closed:{ENDC} Meme aiohttp.ClientSession.")
	else:
		logger.error("Couldn't get cog 'Meme'.")

	# Close the global aiohttp.ClientSession
	await SESSION.close()
	logger.debug(f"{WARNING}Closed:{ENDC} Global aiohttp.ClientSession.")

	em = discord.Embed(
		description="I'm leaving!",
		colour=discord.Colour.green()
	)
	await ctx.send(embed=em)
	# Close the bot
	await bot.close()
	logger.info(f"{GREEN}Bot offline.{ENDC}\n")

	logging.shutdown()


@bot.command(
	name="ping",
	help="Pings the bot, shows its current latency"
)
async def ping_back(ctx: commands.Context):
	"""
	Simple ping command. Has a mini easter egg.
	If the bot is connected to a voice channel, sends the current and average latency.
	"""
	r = random.randint(1, 3)
	# Mini easter egg
	name = "Latency:ping_pong:" if r == 1 else "Latency"

	em = discord.Embed()
	em.add_field(
		name=name,
		value=f"{round(bot.latency * 1000)} ms",
		inline=False
	)

	music = bot.get_cog('Music')

	if music is not None:

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


@bot.command(
	name="test",
	help="Test different functions"
)
@commands.is_owner()
async def test(ctx: commands.Context):
	"""
	Test function.
	The idea is to not have many different test functions
	but change the contents of this one as needed.
	"""
	logger.info("This is a test.")


@bot.command(
	name="version",
	help="Get the bot's current version, use option 'remote' to check the latest version",
	aliases=['ver']
)
@commands.is_owner()
async def check_version(ctx: commands.Context, option: str = "local"):
	"""
	Checks the current bot version.
	Can check the latest release on GitHub.	If the bot's not up to date,
	it shows what type of update (major|minor|patch) is available, the
	corresponding release message, and a link to the releases page.
	Can also get the full release notes with 'notes' option.

	Parameters:
		- option:
			'local' to check only the bot's current version,
			'remote' to check the current version and the repo's latest version,
			'notes' to get the full release notes.
			Defaults to 'local'.
	"""

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
			em = discord.Embed(
				title=f"The bot's current version is {local_ver}",
				description=f"Use `{BOT_PREFIX}version remote` to check for updates."
			)
			await ctx.send(embed=em)

	elif option == "remote":

		# Get remote version
		remote_api_url = "https://api.github.com/repos/JulioLoayzaM/CroissantBot/releases/latest"  # noqa: 501
		header = {'Accept': "application/vnd.github.v3+json"}

		async with SESSION.get(remote_api_url, headers=header) as response:
			latest: dict = await response.json()

		remote_ver = version.parse(latest.get('tag_name'))

		# Determine the embed's colour first - the colour has to be set
		# during initialization, but that would mean creating the embed
		# and adding the version fields on every case.
		if local_ver is None:
			colour = discord.Colour.red()
		else:
			if local_ver == remote_ver:
				colour = discord.Colour.green()
			elif local_ver < remote_ver:
				colour = discord.Colour.gold()
			else:
				colour = discord.Colour.teal()

		# Create the embed with the colour
		em = discord.Embed(colour=colour)

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
					status_message += "**Warning:** a major update may contain breaking changes.\n"
					status_message += "Please check the changelog first, then use `git pull` to update."
					em.add_field(name="Status", value=status_message, inline=False)

				elif local_ver.minor < remote_ver.minor:
					status_message = "A new **minor** version is available. Use `git pull` to update."
					em.add_field(name="Status", value=status_message, inline=False)

				else:
					status_message = "A new **patch** is available. Use `git pull` to update."
					em.add_field(name="Status", value=status_message, inline=False)

				# Extract the message before the patch notes
				body: str = latest.get('body')
				# The notes start with an H2 header
				index = body.index('##')
				release_message = body[:index]
				# The message should contain a couple of newlines at the end - just in case,
				# we get rid of them and add new ones.
				release_message = release_message.rstrip('\r\n')
				release_message += "\n\n"
				release_message += f"Read the release notes with `{BOT_PREFIX}version notes` "
				release_message += "or in the changelog below."

				em.add_field(
					name="Release message",
					value=f"{release_message}",
					inline=False
				)

				changelog_url = "https://github.com/JulioLoayzaM/CroissantBot/releases"
				em.add_field(
					name="Changelog",
					value=changelog_url,
					inline=False
				)

			else:
				status_message = "Your version is more recent than mine! How'd you do that?\n"
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

		async with SESSION.get(remote_api_url, headers=header) as response:
			latest: dict = await response.json()

		remote_ver = version.parse(latest.get('tag_name'))

		title = f"CroissantBot version {remote_ver} release notes:"

		body = latest.get('body')

		em = discord.Embed(title=title, description=body)

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
		em = discord.Embed(
			title="Version options",
			description=message
		)

		await ctx.send(embed=em)


async def check_token() -> bool:
	"""
	Check the validity of TW_TOKEN. If expired or has less than 200 seconds of validity,
	gets a new one, updates the global and .env variables.

	Returns:
		- True if nothing to do/update successful, False otherwise.
	"""

	global TW_TOKEN
	global TW_EXPIRES_IN

	# Check token validity
	validate_url = 'https://id.twitch.tv/oauth2/validate'
	headers = {'Authorization': f"OAuth {TW_TOKEN}"}

	async with SESSION.get(validate_url, headers=headers) as response:
		data: dict = await response.json()

	status = data.get('status')
	# If it can't read the expiration time, assume invalid token.
	TW_EXPIRES_IN = data.get('expires_in', 0)

	# Refresh token if status 401 (means missing or invalid token)
	# or if token is about to expire.
	if (status == 401) or (TW_EXPIRES_IN < 200):

		logger.info(f"Current {PURPLE}TW_TOKEN{ENDC} is invalid, getting a new one.")
		logger.debug(f"Status: {status}, TW_EXPIRES_IN: {TW_EXPIRES_IN}")
		logger.debug(f"Message: {data.get('message', 'no message')}")

		client_id = os.getenv('TW_CLIENT_ID')
		client_secret = os.getenv('TW_CLIENT_SECRET')

		token_url = 'https://id.twitch.tv/oauth2/token'
		body = {
			'client_id': client_id,
			'client_secret': client_secret,
			'grant_type': "client_credentials"
		}

		async with SESSION.post(token_url, data=body) as token_response:
			token_data = token_response.json()

		new_token = token_data.get('access_token', None)

		if new_token is None:
			logger.error("New TW_TOKEN is None.")
			logger.debug(f"token_data: {token_data}")
			return False

		try:
			set_key('.env', 'TW_TOKEN', new_token)
		except Exception as e:
			logger.error("Error while updating TW_TOKEN.")
			logger.debug(f"Could not set the new value in .env:\n{e}")
			return False

		logger.info(f"Updated {PURPLE}TW_TOKEN{ENDC} in '.env'.")

		TW_TOKEN = new_token

	return True


async def init_twitch() -> bool:
	"""
	Initializes tw_prev_status and tw_streamers.
	Runs the token validity check.

	Returns:
		- True if initialization was successful, False if not.
	"""

	global TW_PREV_STATUS
	global TW_STREAMERS

	twitch = bot.get_cog('Twitch')
	if twitch is None:
		logger.error("Could not get 'twitch' cog.")
		return False

	try:
		with open(TW_FILE, 'r') as file:
			ids = json.load(file)

	except IOError as ioe:
		logger.error(f"Could not open \"{TW_FILE}\"")
		logger.debug(f"IOError:\n{ioe}")
		return False

	except Exception as e:
		logger.error(f"Could not open \"{TW_FILE}\"")
		logger.debug(f"Unexpected exception:\n{e}")
		return False

	# Check the token when starting the bot to get the expiration time
	token_status = await check_token()

	if not token_status:
		logger.error("Could not check validity of TW_TOKEN.")
		return False

	TW_STREAMERS = twitch.init_streamers(ids)

	TW_PREV_STATUS = twitch.init_status(TW_STREAMERS)

	if len(TW_STREAMERS) == 0:
		logger.warning("tw_streamers is empty.")
		logger.debug(f"ids: {ids}")
		return False

	if len(TW_PREV_STATUS) == 0:
		logger.warning("tw_prev_status is empty, possible initialization error.")
		logger.debug(f"tw_streamers: {TW_STREAMERS}")
		return False

	return True


@loop(minutes=TW_FREQUENCY)
async def check_twitch():
	"""
	Loop function, calls twitch.check_users every TW_FREQUENCY minutes.
	Sends all messages returned.
	Workaround for Twitch's sometimes unreliable notifications.
	"""

	global TW_PREV_STATUS
	global TW_EXPIRES_IN

	twitch = bot.get_cog('Twitch')
	if twitch is None:
		logger.error("Could not get 'twitch' cog.")
		return

	# TW_FREQUENCY minutes have passed
	TW_EXPIRES_IN -= TW_FREQUENCY * 60

	if TW_EXPIRES_IN < 200:
		check = await check_token()
	else:
		check = True

	if not check:
		logger.warning("TW_TOKEN refresh failed, skipping current check.")
		return

	messages, TW_PREV_STATUS = await twitch.check_users(
		TW_PREV_STATUS, TW_STREAMERS, TW_TOKEN, SESSION
	)

	if messages is None:
		logger.warning("Error checking twitch, waiting for next iteration.")
		return

	for user_id in messages:

		user = bot.get_user(int(user_id))
		message: discord.Embed

		for message in messages[user_id]:

			await user.send(embed=message)
			logger.debug(f"{PURPLE}TW Notif{ENDC} sent to {user.name}: \"{message.title}\"")


@check_twitch.before_loop
async def check_twitch_before():
	"""
	Necessary function: since we start check_twitch before the bot,
	but we need the bot to use get_user and user.send, we wait until
	it's ready.
	"""
	await bot.wait_until_ready()


def init_youtube():
	"""
	Initializes yt_prev_status and yt_streamers.
	"""

	global YT_PREV_STATUS
	global YT_STREAMERS

	youtube = bot.get_cog('Youtube')
	if youtube is None:
		logger.error("Could not get 'youtube' cog.")
		return

	try:
		with open(YT_FILE, 'r') as file:
			ids = json.load(file)

	except IOError as ioe:
		logger.error(f"Could not open {YT_FILE}")
		logger.debug(f"IOError:\n{ioe}")

	except Exception as e:
		logger.error(f"Could not open {YT_FILE}")
		logger.debug(f"Unexpected exception:\n{e}")

	YT_STREAMERS = youtube.init_streamers(ids)

	YT_PREV_STATUS = youtube.init_status(YT_STREAMERS)


@loop(minutes=TW_FREQUENCY)
async def check_youtube():
	"""
	Loop function, calls youtube.check_users every TW_FREQUENCY minutes.
	Sends all messages returned.
	Workaround for Youtube's sometimes unreliable notifications.
	"""

	global YT_PREV_STATUS

	youtube = bot.get_cog('Youtube')
	if youtube is None:
		logger.error("Could not get 'youtube' cog.")
		return

	if len(YT_PREV_STATUS) == 0:
		logger.warning("yt_prev_status is empty, possible initialization error: stopping.")
		return

	if len(YT_STREAMERS) == 0:
		logger.warning("yt_streamers is empty, possible initialization error: stopping.")
		return

	messages, YT_PREV_STATUS = await youtube.check_users(YT_PREV_STATUS, YT_STREAMERS)

	for user_id in messages:

		user = bot.get_user(int(user_id))
		message: discord.Embed

		for message in messages[user_id]:

			await user.send(embed=message)
			logger.debug(f"{PURPLE}YT Notif{ENDC} sent to {user.name}: \"{message.title}\"")


@check_youtube.before_loop
async def check_youtube_before():
	"""
	Necessary function: since we start check_twitch before the bot,
	but we need the bot to use get_user and user.send, we wait until
	it's ready.
	"""
	await bot.wait_until_ready()


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
	"""
	Catches commands' errors, defines corresponding responses.

	Parameters:
		- error: a raised CommandError, not a 'normal' exception.
	"""

	if isinstance(error, commands.CommandNotFound):
		em = discord.Embed(
			title="Error",
			description=f"Command not found, try `{BOT_PREFIX}help`",
			color=ctx.author.color
		)
		await ctx.send(embed=em)

	elif isinstance(error, commands.NoPrivateMessage):
		await ctx.send("You can't use that command in DMs.")

	elif isinstance(error, commands.CheckFailure):
		await ctx.send("You don't have permission to use that command.")

	else:
		logger.error(f"Unexpected command error:\n{error}")


@bot.event
async def on_guild_join(guild: discord.Guild):
	"""
	Logs any new guilds the bot has joined.

	Parameters:
		- the joined guild.
	"""
	logger.debug(f"Joined a guild: {guild.name}.")


def setup_loggers():
	"""
	Sets up the loggers 'CroissantBot' and 'discord'.

	Handlers created:
		- INFO-level to STDOUT
		- INFO-level to a file
		- DEBUG-level to a file
		- discord DEBUG-level to a file
	"""

	global logger
	global discord_logger

	# Creates the CroissantBot logger
	logger = logging.getLogger('CroissantBot')
	logger.setLevel(logging.DEBUG)

	# Gets the discord logger
	discord_logger = logging.getLogger('discord')
	discord_logger.setLevel(logging.DEBUG)

	# Handler - writes INFO logging to stdout
	standard_handler = logging.StreamHandler()
	standard_handler.setLevel(logging.INFO)
	standard_handler.setFormatter(CustomFormatter())

	# Handler - writes INFO logging to file
	info_handler = TimedRotatingFileHandler(
		LOG_INFO_FILE,
		when='midnight',
		backupCount=LOG_COUNT
	)
	info_handler.setLevel(logging.INFO)
	info_handler.setFormatter(CustomFormatter())

	# Handler - writes DEBUG logging to file
	debug_handler = TimedRotatingFileHandler(
		LOG_DEBUG_FILE,
		when='midnight',
		backupCount=LOG_COUNT
	)
	debug_handler.setLevel(logging.DEBUG)
	debug_handler.setFormatter(CustomFormatter())

	# Handler - writes DEBUG discord logging to file
	discord_debug_handler = TimedRotatingFileHandler(
		LOG_DISCORD_FILE,
		when='midnight',
		backupCount=LOG_COUNT
	)
	discord_debug_handler.setLevel(logging.DEBUG)
	discord_debug_handler.setFormatter(CustomFormatter())

	logger.addHandler(standard_handler)
	logger.addHandler(info_handler)
	logger.addHandler(debug_handler)

	discord_logger.addHandler(discord_debug_handler)

	logger.debug(f"{GREEN}Loggers set.{ENDC}")


def fix_logger():
	"""
	Fixes some annoyances caused by streamlink's logging, namely writing unused
	error messages to STDOUT and changing the levelnames to lowercase.
	"""

	# Move streamlink logs to a file
	streamlink_handler = TimedRotatingFileHandler(
		LOG_STREAMLINK_FILE,
		when='midnight',
		backupCount=LOG_COUNT
	)
	streamlink_handler.setLevel(logging.DEBUG)
	logging.getLogger('streamlink').addHandler(streamlink_handler)

	# Restores the uppercase in levelnames
	logging.addLevelName(logging.DEBUG, 'DEBUG')
	logging.addLevelName(logging.INFO, 'INFO')
	logging.addLevelName(logging.WARNING, 'WARNING')
	logging.addLevelName(logging.ERROR, 'ERROR')
	logging.addLevelName(logging.CRITICAL, 'CRITICAL')


async def create_session():
	"""
	Creates the global aiohttp.session, mainly to avoid a DeprecationWarning.
	"""
	global SESSION
	SESSION = aiohttp.ClientSession()


def main(loop: asyncio.AbstractEventLoop):
	"""
	Sets up the bot's start:
		- Sets up the loggers
		- Loads the required cogs: misc, music and meme
		- Loads the twitch and youtube cogs if enabled through .env
		- Starts their corresponding check function
		- Starts running the bot
	"""

	setup_loggers()

	logger.debug(f"{WARNING}Setting up bot...{ENDC}")

	bot.load_extension("cogs.misc")
	bot.load_extension("cogs.music")
	bot.load_extension("cogs.meme")

	# A string to log which cogs got loaded
	enabled_cogs = "misc, music, meme"

	loop.run_until_complete(create_session())

	logger.debug(f"{WARNING}Created:{ENDC} Global aiohttp.ClientSession.")

	# Load the twitch and youtube cogs if enabled
	if TWITCH_ENABLED:
		bot.load_extension("cogs.twitch")
		twitch_initiated = loop.run_until_complete(init_twitch())
		if twitch_initiated:
			check_twitch.start()
			enabled_cogs += f", {PURPLE}twitch{ENDC}"
		else:
			logger.warning(f"Can't enable {PURPLE}twitch{ENDC} cog, unloading extension.")
			bot.unload_extension('cogs.twitch')

	if YOUTUBE_ENABLED:
		bot.load_extension("cogs.youtube")
		init_youtube()
		check_youtube.start()
		enabled_cogs += f", {PURPLE}youtube{ENDC}"
		fix_logger()

	if PLAYLIST_ENABLED:
		bot.load_extension("cogs.playlist")
		enabled_cogs += f", {CYAN}playlist{ENDC}"

	enabled_cogs += "."

	# Log which cogs got loaded
	logger.debug(f"{WARNING}Enabled cogs:{ENDC} {enabled_cogs}")
	logger.debug(f"{WARNING}Bot starting...{ENDC}")

	# Start the bot
	bot.run(BOT_TOKEN)


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	main(loop)
	loop.close()
