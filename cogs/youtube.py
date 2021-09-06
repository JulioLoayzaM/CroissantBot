# youtube.py
#
# Cog to check if a youtube streamer started streaming and send a DM accordingly.
# Uses streamlink to check for active streams.


# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


import json
import logging
import streamlink

from os import getenv
from dotenv import load_dotenv
from typing import Dict, Tuple, Union, List, Set
from discord import Embed
from discord.ext import commands

load_dotenv()

YT_FILE = getenv('YT_FILE')

# 'CroissantBot' logger
logger = None

class Youtube(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	def init_streamers(self, ids: Dict[str, Dict[str, Dict[str, Union[str, List[str]]]]]) -> Dict[str, Dict[str, Union[str, Set[str]]]]:
		"""
		Reverses ids: the streamers become the keys, the values of streamers become the keys' values,
		the recipients are added to the values.

		Returns:
			- a dict following the template:
				{
					'streamer_name': {
						'nickname': "streamer_nickname",
						'url': "streamer_channel",
						'recipients': {
							"discord_user_1",
							"discord_user_2"
						}
					}
				}
		"""

		result: Dict[str, Dict[str, Union[str, List[str]]]] = dict()

		for recipient in ids.keys():

			streamers: Dict[str, Dict[str, Union[str, List[str]]]] = ids[recipient]

			for streamer in streamers.keys():

				if streamer not in result:
					result[streamer] = streamers[streamer]
					result[streamer]['recipients'] = set()

				result[streamer]['recipients'].add(recipient)

		return result


	def init_status(self, streamers: Dict[str, Dict[str, Union[str, Set[str]]]]) -> Dict[str, bool]:
		"""
		Initializes the streamers' status to False/offline.

		Returns:
			- a dict following the template:
				{
					'youtube_user_1': False,
					'youtube_user_2': False
				}
		"""

		status = dict()

		for streamer in streamers.keys():

			status[streamer] = False

		return status


	def check_users(self, prev_status: Dict[str, bool], streamers: Dict[str, Dict[str, Union[str, Set[str]]]]) -> Tuple[Dict[str, List[Embed]], Dict[str, bool]]:
		"""
		Checks the status of streamers and sends a message to a determined user if the streamer just got online.

		Parameters:
			- prev_status: the last known status of the streamers as bool.
			- streamers: the streamers to check and their info, including which users to notify.
		Returns:
			- messages: the messages to be sent, the keys are the discord users.
			- prev_status: updated streamers' status.
		"""

		# messages:
		# {
		#	'discord_user': [embed_1, embed_2, ...]
		# }
		messages: Dict[str, List[Embed]] = dict()

		for streamer in streamers.keys():

			streamer_info = streamers[streamer]

			channel = streamer_info['url']

			# streamlink.streams should not raise an error for a stream,
			# (it does for a protected video) but I already had an error
			# print to stdout so try/except it is.
			try:
				streams = streamlink.streams(channel)
			except streamlink.PluginError as pe:
				logging.getLogger('streamlink.plugin.youtube').warning("Error raised while checking a stream, skipping to next one.")
				logging.getLogger('streamlink.plugin.youtube').debug(f"Channel: {channel}\nError:\n{pe}")
				continue
			except Exception as e:
				logger.debug("Error raised while checking a stream, skipping to next one.")
				logger.debug(f"Channel: {channel}\nError:\n{e}")
				continue

			# If no streams are returned, streamer is Offline
			if len(streams) == 0:
				prev_status[streamer] = False
				continue

			# If something is returned, check if there's a valid stream
			else:
				# Get the stream's best quality url
				best_stream = streams['best']

				url = getattr(best_stream, 'url', None)
				# If url is None, then there's not a valid stream
				if url is None:
					prev_status[streamer] = False
					continue

				# If there's a valid stream, check if streamer was already Online;
				# skip if it's the case
				if prev_status[streamer]:
					continue

				# Else, update the status and proceed
				prev_status[streamer] = True

				# Extract the livestream's ID from the url
				# example: https://something......../id/videoid.X/......
				# where X is a number, but not part of the ID
				start = url.find('/id/')
				tmp = url[start+4:]
				end = tmp.find('.')

				stream_id = tmp[:end]

				stream_url = f"https://www.youtube.com/watch?v={stream_id}"

				nickname = streamer_info['nickname']

				message = f"{stream_url}"

				# Create the embed to be sent
				em = Embed(
					title=f"{nickname} is streaming",
					description=message
				)

				for recipient in streamer_info['recipients']:
					# Append the embed or create the list if it's the first one
					if recipient in messages:
						messages[recipient].append(em)
					else:
						messages[recipient] = [em]

		return messages, prev_status



def setup(bot):
	global logger
	logger = logging.getLogger("CroissantBot")
	bot.add_cog(Youtube(bot))