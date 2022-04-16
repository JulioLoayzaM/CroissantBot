# CroissantBot/cogs/youtube.py

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
import streamlink
import yt_dlp

from typing import Dict, Tuple, Union, List, Set
from discord import Embed
from discord.ext import commands


class Youtube(commands.Cog):
	"""Cog to check the status of youtube livestreamers.

	Check if a youtube streamer started streaming and send a DM accordingly.
	Uses streamlink to check for active streams.
	"""

	def __init__(
		self,
		bot: commands.Bot,
		ydl: yt_dlp.YoutubeDL
	):
		self.bot = bot
		self.ydl = ydl
		self.logger = bot.logger

	def init_streamers(
		self,
		ids: Dict[str, Dict[str, Dict[str, Union[str, List[str]]]]]
	) -> Dict[str, Dict[str, Union[str, Set[str]]]]:
		"""
		Reverses ids: the streamers become the keys, the values of streamers
		become the keys' values, the recipients are added to the values.

		Parameters:
			ids: A dict following the template:
				{
					'streamer_name': {
						'nickname': "streamer_nickname",
						'url': "streamer_channel",
					}
				}

		Returns:
			A dict following the same template as above, but adding a
			'recipients' field, which has a list of all discord users
			to notify about that channel.
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

	def init_status(
		self,
		streamers: Dict[str, Dict[str, Union[str, Set[str]]]]
	) -> Dict[str, bool]:
		"""
		Initializes the streamers' status to False/offline.

		Parameters:
			streamers: The dict returned by init_streamers.

		Returns:
			A dict following the template:
				{
					'youtube_user_1': False,
					'youtube_user_2': False
				}
		"""

		status = dict()

		for streamer in streamers.keys():

			status[streamer] = False

		return status

	async def check_users(
		self,
		prev_status: Dict[str, bool],
		streamers: Dict[str, Dict[str, Union[str, Set[str]]]]
	) -> Tuple[Dict[str, List[Embed]], Dict[str, bool]]:
		"""
		Checks the status of streamers and sends a message to a determined user
		if the streamer just got online.

		Parameters:
			prev_status: The last known status of the streamers as bool.
			streamers: The streamers to check and their info, including which users to notify.

		Returns:
			messages: The messages to be sent, the keys are the discord users.
			prev_status: Updated streamers' status.
		"""

		logger = self.logger

		# messages:
		# {
		#	'discord_user': [embed_1, embed_2, ...]
		# }
		messages: Dict[str, List[Embed]] = dict()

		loop = self.bot.loop or asyncio.get_event_loop()

		for streamer in streamers.keys():

			streamer_info = streamers[streamer]

			channel = streamer_info['url']
			channel += "/live"

			# streamlink.streams should not raise an error for a stream,
			# (it does for a protected video) but I already had an error
			# print to stdout so try/except it is.
			try:
				streams = await loop.run_in_executor(None, streamlink.streams, channel)
			except streamlink.PluginError as pe:
				logging.getLogger('streamlink.plugin.youtube').warning(
					"Error raised while checking a stream, skipping to next one."
				)
				logging.getLogger('streamlink.plugin.youtube').debug(
					f"Channel: {channel}\nError:\n{pe}"
				)
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
				tmp = url[start + 4:]
				end = tmp.find('.')

				stream_id = tmp[:end]

				stream_url = f"https://www.youtube.com/watch?v={stream_id}"

				nickname = streamer_info['nickname']

				metadata = await loop.run_in_executor(
					None, lambda: self.ydl.extract_info(stream_url, download=False)
				)

				stream_title = metadata.get('title')

				stream_thumbnail = metadata.get('thumbnail')

				message = f"{stream_title}\n{stream_url}"

				# Create the embed to be sent
				em = Embed(
					title=f"{nickname} is streaming",
					description=message
				)
				em.set_thumbnail(url=stream_thumbnail)

				for recipient in streamer_info['recipients']:
					# Append the embed or create the list if it's the first one
					if recipient in messages:
						messages[recipient].append(em)
					else:
						messages[recipient] = [em]

		return messages, prev_status


def setup(bot):

	ytdl_options = {
		'nooverwrites': True,
		'restrictfilenames': True,
		'noplaylist': True,
		'nocheckcertificate': True,
		'ignoreerrors': False,
		'logtostderr': False,
		'quiet': True,
		'no_warnings': True,
		'default_search': 'auto',
		'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
	}

	ydl = yt_dlp.YoutubeDL(ytdl_options)

	bot.add_cog(Youtube(bot, ydl))
