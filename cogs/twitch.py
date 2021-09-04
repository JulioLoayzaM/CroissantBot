# twitch.py
#
# Cog to check if a streamer just started streaming and send a DM accordingly.
# Uses the requests library and Twitch's API to get the information.


# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


import requests
import logging
import json

from os import getenv
from typing import Dict, Tuple, List, Set
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TWITCH_API_ENDPOINT = "https://api.twitch.tv/helix/streams?user_login="

TW_CID = getenv('TW_CLIENT_ID')

RES_SESSION = requests.Session()

# 'CroissantBot' logger
logger = None

class Twitch(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	def checkUser(self, userID: str, token: str) -> bool:
		"""
		Deprecated.
		Checks if a single streamer is online.

		Parameters:
			- userID: a Twitch ID to check.
			- token: a valid Twitch API app access token.
		Returns:
			- True if online, False otherwise.
		"""
		url = f"{TWITCH_API_ENDPOINT}{userID}"

		try:
			req = RES_SESSION.get(url, headers={'Client-ID' : TW_CID,'Authorization': f'Bearer {token}'})
			jsondata = req.json()
			if 'stream' in jsondata:
				if jsondata['stream'] is not None: #stream is online
					return True
				else:
					return False

		except Exception as e:
			logger.error("Error in request.")
			logger.debug(f"Unexpected exception:\n{e}")
			return False


	def init_streamers(self, ids: Dict[str, List[str]]) -> Dict[str, Set[str]]:
		"""
		Reverses ids: the streamers become the keys, the recipients become the values.

		Returns:
			- a dict following the template:
				{
					"twitch_user_1": {
						"discord_user_1",
						"discord_user_2"
					},
					"twitch_user_2": {
						"discord_user_1",
						"discord_user_3"
					}
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

		Returns:
			- a dict following the template:
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


	def check_users(self, prev_status: Dict[str, bool], streamers: Dict[str, List[str]], token: str) -> Tuple[Dict[str, Embed], Dict[str, bool]]:
		"""
		Checks the status of streamers and sends a message to a determined user if the streamer just got online.

		Parameters:
			- prev_status: the last known status of the streamers as bool.
			- streamers: the streamers to check and the corresponding users to notify.
			- token: a valid Twitch API app access token.
		Returns:
			- messages: the Embeds to be sent, the keys are the discord users.
			- prev_status: updated streamers' status.
		If the token isn't valid, returns (None, prev_status). bot.check_twitch should handle
		the token refresh.
		"""

		headers = {
			'Client-ID' : TW_CID,
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
			req = RES_SESSION.get(url, headers=headers)
		except Exception as e:
			logger.error("Error in GET request.")
			logger.debug(f"Unexpected exception:\n{e}")
			logger.warning("Skipping current check.")
			return (None, prev_status)

		jsondata = req.json()

		error = jsondata.get('error')

		if error is not None:
			status = jsondata.get('status')
			message = jsondata.get('message')
			logger.error("Can't reach API endpoint.")

			# 401 means missing or invalid access token - return and get another token during the next check
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

			# example: https://static-cdn.jtvnw.net/previews-ttv/live_user_username-{width}x{height}.jpg
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


	def close_session(self) -> bool:
		"""
		Closes the requests session. Called on bot exit.
		"""
		RES_SESSION.close()
		return True



def setup(bot):
	global logger
	logger = logging.getLogger("CroissantBot")
	bot.add_cog(Twitch(bot))