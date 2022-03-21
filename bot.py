# croissantbot/bot.py

"""Extension of commands.bot.


You may use, distribute and modify this code under
the terms of the MIT license.

See the LICENSE file for more details.
"""

import aiofiles
import aiohttp
import asyncio
import json
import logging
import os

import discord
from discord.ext import commands

from dotenv import set_key


# Colours for formatting console text
GREEN     = '\033[92m'
PURPLE    = '\033[95m'
ENDC      = '\033[0m'


class CroissantBot(commands.Bot):
	"""Extension of a Bot.

	Most env variables are loaded once and stores as attributes.
	"""

	def __init__(
		self,
		prefix: str,
		intents: discord.Intents,
		logger: logging.Logger
	):
		"""Init for CroissantBot

		Mostly initializes the attributes, just a ClientSession is created.
		"""

		super().__init__(command_prefix=prefix, intents=intents)

		self._prefix  = prefix
		self._session = aiohttp.ClientSession()
		# Twitch
		self._tw_file        = None
		self._tw_token       = ''
		self._tw_expires_in  = 0
		self._tw_frequency   = 0
		self._tw_prev_status = None
		self._tw_streamers   = None
		# Youtube
		self._yt_file        = None
		self._yt_prev_status = None
		self._yt_streamers   = None
		# Logger
		self.logger  = logger
		# Cogs
		self.enabled_cogs = list()
		# Background tasks
		self._tw_task = None
		self._yt_task = None

	async def on_ready(self):
		"""
		Informs when the bot is connected, logs the guilds it's currently connected to.
		"""
		self.logger.info(f"{GREEN}{self.user.name} online and connected to Discord.{ENDC}")
		guilds = ', '.join([guild.name for guild in self.guilds])
		self.logger.debug(f"{GREEN}Connected to:{ENDC} {guilds}.")

	async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
		"""
		Catches commands' errors, defines corresponding responses.

		Parameters:
			error: A raised CommandError, not a 'normal' exception.
		"""

		if isinstance(error, commands.CommandNotFound):
			em = discord.Embed(
				title="Error",
				description=f"Command not found, try `{self._prefix}help`",
				color=ctx.author.color
			)
			await ctx.send(embed=em)

		elif isinstance(error, commands.NoPrivateMessage):
			await ctx.send("You can't use that command in DMs.")

		elif isinstance(error, commands.CheckFailure):
			await ctx.send("You don't have permission to use that command.")

		elif isinstance(error, commands.DisabledCommand):
			await ctx.send("This command is currently disabled.")

		else:
			self.logger.error(f"Unexpected command error:\n{error}")

	async def check_token(self) -> bool:
		"""Check the validity of _tw_token.

		If expired or has less than 200 seconds of validity,
		gets a new one, updates the global and .env variables.

		Returns:
			True if nothing to do/update successful, False otherwise.
		"""

		logger = self.logger

		# Check token validity
		validate_url = 'https://id.twitch.tv/oauth2/validate'
		headers = {'Authorization': f"OAuth {self._tw_token}"}

		async with self._session.get(validate_url, headers=headers) as response:
			data: dict = await response.json()

		status = data.get('status')
		# If it can't read the expiration time, assume invalid token.
		self._tw_expires_in = data.get('expires_in', 0)

		# Refresh token if status 401 (means missing or invalid token)
		# or if token is about to expire.
		if (status == 401) or (self._tw_expires_in < 200):

			logger.info(f"Current {PURPLE}TW_TOKEN{ENDC} is invalid, getting a new one.")
			logger.debug(f"Status: {status}, TW_EXPIRES_IN: {self._tw_expires_in}")
			logger.debug(f"Message: {data.get('message', 'no message')}")

			client_id = os.getenv('TW_CLIENT_ID')
			client_secret = os.getenv('TW_CLIENT_SECRET')

			token_url = 'https://id.twitch.tv/oauth2/token'
			body = {
				'client_id': client_id,
				'client_secret': client_secret,
				'grant_type': "client_credentials"
			}

			async with self._session.post(token_url, data=body) as token_response:
				token_data: dict = await token_response.json()

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

			self._tw_token = new_token

		return True

	async def init_youtube(self) -> bool:
		"""Initializes yt_prev_status and yt_streamers.

		Returns:
			True if initialization was successful, False if not.
		"""

		logger = self.logger

		self._yt_file = os.getenv('YT_FILE')
		self._tw_frequency = int(os.getenv('TW_FREQUENCY'))

		youtube = self.get_cog('Youtube')
		if youtube is None:
			logger.error("Could not get 'youtube' cog.")
			return False

		try:
			async with aiofiles.open(self._yt_file, mode='r') as file:
				content = await file.read()

			ids = json.loads(content) if content else dict()

		except IOError as ioe:
			logger.error(f"Could not open {self._yt_file }")
			logger.debug(f"IOError:\n{ioe}")
			return False

		except Exception as e:
			logger.error(f"Could not open {self._yt_file }")
			logger.debug(f"Unexpected exception:\n{e}")
			return False

		self._yt_streamers   = youtube.init_streamers(ids)
		self._yt_prev_status = youtube.init_status(self._yt_streamers)

		# MAYBE: check if the dictionnaries are empty?
		return True

	async def init_twitch(self) -> bool:
		"""Initializes tw_prev_status and tw_streamers.

		Runs the token validity check.

		Returns:
			True if initialization was successful, False if not.
		"""

		logger = self.logger

		self._tw_file  = os.getenv('TW_FILE')
		self._tw_token = os.getenv('TW_TOKEN')
		self._tw_frequency = int(os.getenv('TW_FREQUENCY'))

		twitch = self.get_cog('Twitch')
		if twitch is None:
			logger.error("Could not get 'twitch' cog.")
			return False

		try:
			async with aiofiles.open(self._tw_file, mode='r') as file:
				content = await file.read()

			ids = json.loads(content) if content else dict()

		except IOError as ioe:
			logger.error(f"Could not open \"{self._tw_file}\"")
			logger.debug(f"IOError:\n{ioe}")
			return False

		except Exception as e:
			logger.error(f"Could not open \"{self._tw_file}\"")
			logger.debug(f"Unexpected exception:\n{e}")
			return False

		# Check the token when starting the bot to get the expiration time
		token_status = await self.check_token()

		if not token_status:
			logger.error("Could not check validity of TW_TOKEN.")
			return False

		self._tw_streamers   = twitch.init_streamers(ids)
		self._tw_prev_status = twitch.init_status(self._tw_streamers)

		if len(self._tw_streamers) == 0:
			logger.warning("tw_streamers is empty.")
			logger.debug(f"ids: {ids}")
			return False

		if len(self._tw_prev_status) == 0:
			logger.warning("tw_prev_status is empty, possible initialization error.")
			logger.debug(f"tw_streamers: {self._tw_prev_status}")
			return False

		return True

	async def check_twitch(self):
		"""Check the status of twitch livestreamers.

		Loop function, calls twitch.check_users every self._tw_frequency minutes.
		Sends all messages returned.
		Workaround for Twitch's sometimes unreliable notifications.
		"""

		# get_user and user.send require the bot to be ready, so wait
		# before actually starting the function
		await self.wait_until_ready()

		logger = self.logger

		twitch = self.get_cog('Twitch')
		if twitch is None:
			logger.error("Could not get 'twitch' cog.")
			return

		while not self.is_closed():

			# _tw_frequency minutes have passed
			self._tw_expires_in -= self._tw_frequency * 60

			check = await self.chech_token() if self._tw_expires_in < 200 else True

			if not check:
				logger.warning("TW_TOKEN refresh failed, skipping current check.")
				# instead of using continue, emulate a successful loop
				# that way, we don't end up in a 0-delay loop
				await asyncio.sleep(self._tw_frequency * 60)
				continue

			messages, self._tw_prev_status = await twitch.check_users(
				self._tw_prev_status, self._tw_streamers, self._tw_token, self._session
			)

			if messages is None:
				logger.warning("Error checking twitch, waiting for next iteration.")
				await asyncio.sleep(self._tw_frequency * 60)
				continue

			for user_id in messages:
				user = self.get_user(int(user_id))
				message: discord.Embed
				for message in messages[user_id]:
					await user.send(embed=message)
					logger.debug(f"{PURPLE}TW Notif{ENDC} sent to {user.name}: \"{message.title}\"")

			await asyncio.sleep(self._tw_frequency * 60)

	async def check_youtube(self):
		"""Check the status of youtube livestreamers.

		Loop function, calls youtube.check_users every self._tw_frequency minutes.
		Sends all messages returned.
		Workaround for Youtube's sometimes unreliable notifications.
		"""

		await self.wait_until_ready()

		logger = self.logger

		youtube = self.get_cog('Youtube')
		if youtube is None:
			logger.error("Could not get 'youtube' cog")
			return

		if len(self._yt_prev_status) == 0:
			logger.warning("yt_prev_status is empty, possible initialization error: stopping.")
			return

		if len(self._yt_streamers) == 0:
			logger.warning("yt_streamers is empty, possible initialization error: stopping.")
			return

		while not self.is_closed():

			messages, self._yt_prev_status = await youtube.check_users(
				self._yt_prev_status, self._yt_streamers
			)

			for user_id in messages:
				user = self.get_user(int(user_id))
				message: discord.Embed
				for message in messages[user_id]:
					await user.send(embed=message)
					logger.debug(f"{PURPLE}YT Notif{ENDC} sent to {user.name}: \"{message.title}\"")

			await asyncio.sleep(self._tw_frequency * 60)
