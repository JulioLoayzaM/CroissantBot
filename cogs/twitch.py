# CroissantBot/cogs/twitch.py

# Copyright (C) 2021-present JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


import aiofiles
import aiohttp
import json

from os import getenv
from typing import Dict, Tuple, List, Set

import discord
from discord import Embed
from discord.ext import commands


class Twitch(commands.Cog):
	"""Cog to check the status of twitch livestreamers.

	Check if a streamer just started streaming and send a DM accordingly.
	Uses the requests library and Twitch's API to get the information.
	"""

	def __init__(
		self,
		bot: commands.Bot,
		endpoint: str,
		client_id: str
	):
		# Bot attributes
		self.bot     = bot
		self.logger  = bot.logger
		self.session = bot._session
		# Cog attributes
		self.endpoint = endpoint
		self.cid      = client_id

	def init_streamers(self, ids: Dict[str, List[str]]) -> Dict[str, Set[str]]:
		"""
		Reverses ids: the streamers become the keys, the recipients become the values.

		Parameters:
			ids: the dict containing the users to notify and the respective channels to check.
				{
					"discord_user": [
						"twitch_channel_1",
						"twitch_channel_2"
					]
				}

		Returns:
			A dict following the template:
				{
					"twitch_user_1": [
						"discord_user_1",
						"discord_user_2"
					],
					"twitch_user_2": [
						"discord_user_1",
						"discord_user_3"
					]
				}
		"""
		streamers = dict()

		for recipient in ids:

			for user in ids[recipient]:

				# Extract the user_login if an URL is provided.
				temp = user.split('/')
				user_login = temp[-1]

				if user_login not in streamers:
					streamers[user_login] = set()

				streamers[user_login].add(recipient)

		return streamers

	def init_status(self, streamers: Dict[str, Set[str]]) -> Dict[str, bool]:
		"""
		Initializes the streamers' status as False/offline.

		Parameters:
			streamers: The dict returned by init_streamers.

		Returns:
			A dict following the template:
				{
					'twitch_user_1': False,
					'twitch_user_2': False,
					'twitch_user_3': False
				}
		"""
		status = dict()

		for streamer in streamers.keys():

			status[streamer] = False

		return status

	async def check_users(
		self,
		prev_status: Dict[str, bool],
		streamers: Dict[str, Set[str]],
		token: str,
		session: aiohttp.ClientSession
	) -> Tuple[Dict[str, Embed], Dict[str, bool]]:
		"""
		Checks the status of streamers and sends a message to a determined user
		if the streamer just got online.

		Parameters:
			prev_status: The last known status of the streamers as bool.
			streamers: The streamers to check and the corresponding users to notify.
			token: A valid Twitch API app access token.
			session: An aiohttp session to perform the requests with.

		Returns:
			messages: The embeds to be sent, the keys are the discord users.
			prev_status: Updated streamers' status.

		Note:
			If the token isn't valid, returns (None, prev_status). bot.check_twitch should handle
			the token refresh.
		"""

		logger = self.logger
		TW_CID = self.cid
		TWITCH_API_ENDPOINT = self.endpoint

		headers = {
			'Client-ID': TW_CID,
			'Authorization': f'Bearer {token}'
		}

		# messages:
		# {
		#	'discord_user': [embed_1, embed_2, ...]
		# }
		messages = dict()

		online_streamers = set()

		url = TWITCH_API_ENDPOINT + "&user_login=".join(streamers.keys())

		try:
			async with session.get(url, headers=headers) as response:
				jsondata = await response.json()
		except Exception as e:
			logger.error("Error GETting twitch streamers info.")
			logger.debug(f"Unexpected exception:\n{e}")
			logger.warning("Skipping current check.")
			return (None, prev_status)

		error = jsondata.get('error')

		if error is not None:
			status = jsondata.get('status')
			message = jsondata.get('message')
			logger.error("Can't reach Twitch API endpoint.")

			# 401 means missing or invalid access token:
			# return and get another token during the next check
			logger.debug(f"Status {status}: {error}:{message}")
			logger.warning("Skipping current check.")
			return (None, prev_status)

		# data is a list of streams
		data = jsondata.get('data', list())

		for stream in data:

			streamer = stream['user_login']
			online_streamers.add(streamer)

			# If the user was already online, do nothing
			if prev_status[streamer]:
				continue

			# And get the stream info
			title = stream['title']
			username = stream['user_name']
			game = stream['game_name']

			stream_url = f"https://www.twitch.tv/{streamer}"

			# example:
			# https://static-cdn.jtvnw.net/previews-ttv/live_user_username-{width}x{height}.jpg
			temp: str = stream['thumbnail_url']
			# Since we don't need/want to specify the width/height, we remove it from the url
			thumbnail: str = temp.replace("-{width}x{height}", "")

			# Create the embed
			em = Embed(
				title=f"{username} is streaming {game}",
				description=f"{title}\n{stream_url}"
			)
			em.set_thumbnail(url=thumbnail)

			for recipient in streamers[streamer]:
				# Append the embed or create the list if it's the first one
				if recipient in messages:
					messages[recipient].append(em)
				else:
					messages[recipient] = [em]

		# Update prev_status using list of online streamers.
		for streamer in streamers:
			prev_status[streamer] = (streamer in online_streamers)

		return messages, prev_status

	async def user_exists(
		self,
		streamer: str,
		token: str,
		session: aiohttp.ClientSession
	) -> bool:
		"""
		Checks if a streamer exists.

		Arguments:

		streamer:
			The streamer to check. The function calling user_exists must ensure
			it passes an username and not a URL.
		token:
			The API token to use.
		session:
			The aiohttp session to do the request with.

		Returns:

		True if the streamer exists, False if not or in case of error.
		"""

		logger = self.logger
		TW_CID = self.cid
		ENDPOINT = self.endpoint

		headers = {
			'Client-ID': TW_CID,
			'Authorization': f'Bearer {token}'
		}

		url = ENDPOINT + streamer

		try:
			async with session.get(url, headers=headers) as response:
				jsondata = await response.json()
		except Exception as error:
			logger.error("Error GETting twitch streamer info.")
			logger.debug(f"Unexpected exception:\n{error}")
			return False

		error = jsondata.get("error", None)
		if error is not None:
			status = jsondata.get('status', None)
			message = jsondata.get('message', None)
			if status == 401:
				logger.error("Can't reach Twitch API endpoint, bad token.")
			logger.debug(f"Status {status}, {error}:{message}")
			logger.debug(f"Streamer {streamer} not found.")
			return False

		# This should be enough verification that the user exists.
		return True

	@commands.command(
		name="add_streamer",
		help="Add a streamer to your Twitch check list",
		aliases=["add"]
	)
	async def add_streamer(
		self,
		ctx: commands.Context,
		streamer: str,
		user: discord.Member = None
	):
		"""
		Adds a streamer to a user's check list.
		"""

		# supress the embed generate by a URL
		await ctx.message.edit(suppress=True)

		logger = self.logger
		TW_STREAMERS = self.bot._tw_streamers
		TW_PREV_STATUS = self.bot._tw_prev_status
		TW_FILE = self.bot._tw_file

		if 'TWITCH' not in self.bot.enabled_cogs:
			em = discord.Embed(
				description="The Twitch extension is not enabled.",
				colour=discord.Colour.red()
			)
			await ctx.send(embed=em)
			return

		if user is None:
			user: discord.Member = ctx.author
		elif user not in ctx.guild.members:
			em = discord.Embed(
				description="That user doesn't exist or is not in this server.",
				colour=discord.Colour.red()
			)
			await ctx.send(embed=em)
			return

		uid = str(user.id)

		# A simple test to check whether the string passed is a URL
		# or just the name of the streamer.
		if streamer.find('/'):
			streamer = streamer.split('/')[-1]

		twitch = self.bot.get_cog('Twitch')
		if twitch is None:
			em = discord.Embed(
				description="An error occurred, please try again.",
				colour=discord.Colour.red()
			)
			await ctx.send(embed=em)
			logger.error("Can't use Twitch cog.")
			logger.debug("TW_ENABLE flag checked, so the cog should be usable.")
			return

		user_exists: bool = await twitch.user_exists(
			streamer, self.bot._tw_token, self.session
		)

		if user_exists:
			# Add the (streamer, user) couple to TW_STREAMERS.
			if streamer in TW_STREAMERS:
				users: Set[str] = TW_STREAMERS.get(streamer)
				# If the streamer was already in the user's list, return.
				if uid in users:
					em = discord.Embed(
						description=f"{streamer} is already in your list!",
						colour=discord.Colour.green()
					)
					await ctx.send(embed=em)
					return
				else:
					users.add(uid)
			else:
				TW_STREAMERS[streamer] = {uid}

			# Then add the streamer to TW_PREV_STATUS.
			if streamer not in TW_PREV_STATUS:
				TW_PREV_STATUS[streamer] = False

			# And finally, add it to the file.
			try:
				async with aiofiles.open(TW_FILE, 'r') as file:
					content = await file.read()

				ids = json.loads(content) if content else dict()

				if uid in ids:
					streamers = ids.get(uid)
					streamers.append(streamer)
				else:
					ids[uid] = [streamer]

				dump = json.dumps(ids)
				async with aiofiles.open(TW_FILE, 'w') as file:
					await file.write(dump)

			except Exception as error:
				logger.error("Couldn't add streamer to TW_FILE.")
				logger.debug(f"Unexpected exception:\n{error}")
				em = discord.Embed(
					description="""
						Couldn't find that user, please check you've got the
						right username or URL.
					""",
					colour=discord.Colour.gold()
				)
				await ctx.send(embed=em)
				return

			em = discord.Embed(
				description=f"""
					Added streamer {streamer} to your list!
				""",
				colour=discord.Colour.green()
			)
			await ctx.send(embed=em)

		else:
			em = discord.Embed(
				description="""
					Couldn't find that user, please check you've got the
					right username or URL.
				""",
				colour=discord.Colour.gold()
			)
			await ctx.send(embed=em)


def setup(bot):

	api_endpoint = "https://api.twitch.tv/helix/streams?user_login="
	client_id = getenv('TW_CLIENT_ID')

	bot.add_cog(Twitch(bot, api_endpoint, client_id))
