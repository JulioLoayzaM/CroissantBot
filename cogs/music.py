# music.py
#
# Cog for music related commands.


# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


# The MIT License (MIT)

# Copyright (c) 2015-present Rapptz

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


import aiofiles
import asyncio
import json
import logging
import os
import youtube_dl


import discord
from discord.ext import commands

from cogs.queue import SongQueue
from cogs.song import Song

from dotenv import load_dotenv
from typing import Tuple, Union, List, Dict



# Colours and string for some coloured output
BLUE = '\033[94m'
ENDC = '\033[0m'
VOICE = f"{BLUE}[voice]{ENDC}"


load_dotenv()
# Videos longer than MAX_DURATION seconds won't be downloaded
MAX_DURATION = int(os.getenv('MAX_DURATION'))
# Directory in which music is downloaded
SAVE_DIR = os.getenv('MUSIC_DIR')
# Name of the file in which the list of favourites is kept - 'rsc/favourite_songs.json' by default
FAV_LIST_FILE = f"rsc/{os.getenv('MUSIC_FAV_LIST', 'favourite_songs.json')}"

BOT_PREFIX = os.getenv('BOT_PREFIX')

FAV_LIST = None

# 'CroissantBot' logger
logger = None


# Used to suppress useless errors apparently
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
	'outtmpl': f'{SAVE_DIR}/%(title)s-%(id)s.%(ext)s',
	'nooverwrites': True,
	'format': 'bestaudio/best',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
	'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Music(commands.Cog):

	def __init__(self, bot: commands.Bot):

		self.bot = bot
		# Template:
		# {
		# 	guild_id: {
		# 		channel: discord.TextChannel = None,
		# 		queue: SongQueue = None,
		# 		volume: float = 0.5,
		#		source: discord.AudioSource = None
		# 	}
		# }
		self.info = dict()


	@commands.command(
		aliases=['j'],
		help="Tells the bot to join your current voice channel"
	)
	@commands.bot_has_guild_permissions(connect=True, speak=True)
	@commands.guild_only()
	async def join(self, ctx: commands.Context):
		"""
		Joins the calling user's current voice channel if the user is connected to one.
		"""

		if not ctx.message.author.voice:
			await ctx.send("You're not connected to a voice channel, join one first.")

		else:
			gid = ctx.message.guild.id
			channel = ctx.author.voice.channel
			# If the bot is joining a voice channel in this guild for the first time in this session,
			# create the corresponding info dict
			if gid not in self.info:
				self.info[gid] = {
					'channel': None,
					'queue': None,
					'volume': 0.5,
					'source': None
				}

			current_info = self.info[gid]

			# channel != None means the bot is connected to a channel
			if current_info['channel'] is not None:
				if current_info['channel'].name == channel.name:
					await ctx.send(f"The bot is already connected to {channel.name}.")
				else:
					await ctx.send(f"The bot is already connected to {current_info['channel'].name}. You can try `{BOT_PREFIX}move_here` if that channel is empty.")
				return

			current_info['channel'] = channel
			new_queue = SongQueue()
			current_info['queue'] = new_queue

			logger.debug(f"{VOICE} Connecting to \"{channel}\"")

			try:
				voice = await channel.connect()
				logger.debug(f"{VOICE} Connected to \"{channel}\"")

			except asyncio.TimeoutError as ate:
				logger.error(f"Could not connect to voice channel in time.")
				logger.debug(f"asyncio.TimeoutError:\n{ate}")

			except discord.ClientException as ce:
				logger.warning(f"Already connected to voice channel.")
				logger.debug(f"discord.ClientException:\n{ce}")

			except discord.opus.OpusNotLoaded as onl:
				logger.error(f"Opus library not loaded.")
				logger.debug(f"discord.opus.OpusNotLoaded:\n{onl}")

			except Exception as e:
				logger.error(f"Couldn't connect to \"{channel}\".")
				logger.debug(f"Unexpected exception:\n{e}")


	@commands.command(
		help="Tells the bot to disconnect from its current voice channel"
	)
	@commands.guild_only()
	async def leave(self, ctx: commands.Context):
		"""
		Disconnects from its current voice channel in the calling user's guild.
		Calls stop() to stop audio and clear the queue, and handles the cleaning of channel info.
		"""

		vc: discord.VoiceClient = ctx.message.guild.voice_client
		gid = ctx.message.guild.id
		channel = self.info[gid]['channel']

		if vc.is_connected():

			await self.stop(ctx, leaving=True)

			self.info[gid]['channel'] = None

			await vc.disconnect()

			logger.debug(f"{VOICE} Left \"{channel.name}\"")

		else:

			await ctx.send("The bot is not connected to a voice channel.")


	async def get_queue(self, ctx: commands.Context) -> Union[SongQueue, None]:
		"""
		Gets the current context queue.

		Returns:
			- the corresponding queue, None if not connected to a voice channel.
		"""
		guild_id = ctx.message.guild.id

		# Return None if the guild is not in info, meaning the bot is not connected
		# to a voice channel in that guild
		if guild_id not in self.info:
			return None

		queue = self.info[guild_id]['queue']
		return queue


	@commands.command(
		aliases=['p'],
		help=f"Plays a song from an URL or a search query, use `{BOT_PREFIX}search_youtube <query>` to get more results"
	)
	@commands.guild_only()
	async def play(self, ctx: commands.Context, query: str=None):
		"""
		This function searches youtube and passes the first result URL to play,
		and is in charge of downloading the audio, creating the Song instance and queueing the song.
		Additionally, if no song is playing it calls play_song() to start streaming.

		Parameters:
			- query: the query to search for in youtube.
		"""
		if query is None:
			await ctx.send(f"You have to provide a youtube url or query. Type `{BOT_PREFIX}play <url/query>`.")
			return

		# To avoid clutter, we edit the user's message to suppress the embed
		msg = ctx.message
		await msg.edit(suppress=True)

		loop = self.bot.loop or asyncio.get_event_loop()

		# Checks if query is a valid url, if not we search youtube for the query
		if not await validate_url(query):
			info = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{query}", download=False))
			video = info['entries'][0]
			query = video['webpage_url']

		# We know the query must be a valid url
		url = query

		try :
			guild = ctx.message.guild
			vc = guild.voice_client

			queue = await self.get_queue(ctx)

			if queue is None:
				await ctx.send("The bot is not connected to a voice channel.")
				return

			song = await YTDLSource.from_url(url, loop=self.bot.loop)

			queue.push(song)

			# If a song is playing or paused but not stopped, send a message
			# to indicate the song is queued
			if vc.is_playing() or vc.is_paused():
				dem = {
					"title": "Queued:",
					"description": f"{song.title} - <{song.url}>",
					"colour": ctx.author.color
				}
				em = discord.Embed.from_dict(dem)
				em.set_thumbnail(url=song.thumbnail)
				await ctx.send(embed=em)

			# If no song is playing, we call play_song to start the queue
			else:
				await self.play_song(ctx)

		except MaxDurationError as mde:
			await ctx.send(f"The song is too long (> {int(MAX_DURATION/60)} min), please try another link.")

		except discord.DiscordException as de:
			await ctx.send(f"The bot is not connected to a voice channel, use `{BOT_PREFIX}join`.")
			logger.warning(f"The bot is probably not connected to a voice channel.")
			logger.debug(f"discord.DiscordException:\n{de}")

		except Exception as e:
			logger.error(f"Couldn't play song.")
			logger.debug(f"Unexpected exception:\n{e}")
			await ctx.send("The bot is not connected to a voice channel.")


	@commands.command(
	aliases=['pf'],
	help=f"Sorry this command has been deprecated, please try `{BOT_PREFIX}play`."
	)
	@commands.guild_only()
	async def play_from(self, ctx: commands.Context, url: str=None):
		"""
		Function to notify previous users that the command is now deprecated.
		and passes the url, if given, to the actual play function.

		Parameters:
			- url: the url to search for in youtube.
		"""
		if url is None:
			await ctx.send(f"Sorry this command has been deprecated, please try `{BOT_PREFIX}play` next time.")
			await ctx.send(f"Also, you have to provide a youtube url or query. Type `{BOT_PREFIX}play <url/query>`.")
			return

		await ctx.send(f"Sorry this command has been deprecated, please try `{BOT_PREFIX}play` next time.")
		await self.play(ctx, url)


	@play.before_invoke
	@play_from.before_invoke
	async def ensure_voice(self, ctx: commands.Context):
		"""
		Checks if the bot is connected to the voice channel before playing.
		If not connected, calls join.
		"""
		if ctx.voice_client is None:
			await self.join(ctx)


	async def play_song(self, ctx: commands.Context):
		"""
		Higher function, calls play_next and sends the message it receives.
		"""

		guild = ctx.message.guild
		vc: discord.VoiceClient = guild.voice_client

		def play_next() -> Tuple[Union[str, None], Union[discord.Embed, None]]:
			"""
			Function in charge of actually playing a song.
			It assumes three things:
				- the songs in the queue are already downloaded
				- if a song is playing and we called play_song anyway, we want to skip the song
				- the bot is actually connected to a voice channel

			Returns:
				- an error message if an error occured, None otherwise
				- None if an error occured, an Embed with the song info otherwise
			"""

			# Have to manually get the queue
			gid = ctx.message.guild.id
			queue: SongQueue = self.info[gid]['queue']

			if queue is None:
				logger.warning(f"No queue")
				return "Error: no queue", None

			song = queue.pop()
			# If song is None, it means that the queue is empty
			if song is None:
				vc.stop()
				return f"The queue is empty, use `{BOT_PREFIX}play`", None

			# Skipping a song if one is playing or paused
			if vc.is_playing() or vc.is_paused():
				vc.stop()
				dem = {
					"title": "Skipping to:",
					"description": f"{song.title} - <{song.url}>",
					"colour": ctx.author.color
				}

			else:
				# Starting the queue
				dem = {
					"title": "Now playing:",
					"description": f"{song.title} - <{song.url}>",
					"colour": ctx.author.color
				}

			em = discord.Embed.from_dict(dem)
			em.set_thumbnail(url=song.thumbnail)

			source = YTDLSource(discord.FFmpegPCMAudio(source=song.file), song=song, volume=self.info[gid]['volume'])
			self.info[gid]['source'] = source

			try:
				vc.play(source, after = lambda e: play_next())

			except Exception as e:
				logger.error(f"Couldn't play song.")
				logger.debug(f"Unexpected exception:\n{e}")

			return None, em

		with ctx.typing():
			res, em = play_next()

		if em is None:
			await ctx.send(res)

		else:
			await ctx.send(embed=em)


	@commands.command(
		help="Pauses the currently playing song"
	)
	@commands.guild_only()
	async def pause(self, ctx: commands.Context):
		"""
		Pauses the song if connected and playing, else sends a message to the user.
		"""
		voice_client: discord.VoiceClient = ctx.message.guild.voice_client

		if voice_client.is_connected():

			if voice_client.is_playing():
				voice_client.pause()

			else:
				await ctx.send(f"The bot is not currently playing something, try `{BOT_PREFIX}play`")

		else:
			await ctx.send(f"The bot is not connected to a voice channel, try `{BOT_PREFIX}join`.")


	@commands.command(
		aliases=['res'],
		help="Resumes a paused song"
	)
	@commands.guild_only()
	async def resume(self, ctx: commands.Context):
		"""
		If there's a paused song, it resumes playing it.
		If not, it tries to restart the queue by calling play_song().
		"""

		voice_client = ctx.message.guild.voice_client

		if voice_client.is_connected():

			queue: SongQueue = await self.get_queue(ctx)

			# queue being None is different than queue being empty
			if queue is None:
				await ctx.send("The bot is not connected to a voice channel.")

			# If paused, resume
			elif voice_client.is_paused():
				voice_client.resume()

			# if not paused, restart the queue
			elif not queue.is_empty():
				await ctx.send("The bot was not playing something, resuming from queue.")
				await self.play_song(ctx)

			else:
				await ctx.send("The bot was not playing something and the queue is empty.")

		else:
			await ctx.send(f"The bot is not connected to a voice channel, try `{BOT_PREFIX}join`.")


	@commands.command(
		help="Stops the currently playing (or paused) song and clears the queue"
	)
	@commands.guild_only()
	async def stop(self, ctx: commands.Context, leaving: bool = False):
		"""
		If connected it stops the voice client and clears the queue with the SongQueue method.
		Stops any playing/paused song. Deletes the queue if leaving the voice channel.

		Parameters:
			- leaving: indicates if the function was called by leave(), in which case it doesn't send a "nothing is playing"
				message and DELETES (after clearing) the queue by setting it to None.
		"""

		vc: discord.VoiceClient = ctx.message.guild.voice_client
		queue = await self.get_queue(ctx)
		playing = False

		if queue is None:
			await ctx.send("The bot is not connected to a voice channel.")

		elif vc.is_connected():

			gid = ctx.message.guild.id

			if vc.is_playing() or vc.is_paused():
				playing = True

			vc.stop()	# does it raise an exception if not playing?
			queue.clear()

			if leaving:
				self.info[gid]['queue'] = None

			elif not playing:
				await ctx.send("The bot is not playing anything at the moment, queue cleared.")

		else:
			await ctx.send(f"The bot is not connected to a voice channel, try `{BOT_PREFIX}join`.")


	async def stop_all(self) -> bool:
		"""
		Closes all voice clients and clears self.info, manually.
		Used by close_connection when closing the bot, to ensure no mess is left behind.

		Returns:
			- True if it cleaned anything, False otherwise.
		"""

		if not self.info:
			return False

		# MAYBE: remove stop and disconnect since bot.close calls disconnect
		# and disconnect calls stop.
		for gid in self.info:

			info = self.info[gid]

			channel = info['channel']
			if channel is not None:
				guild = channel.guild
				vc = guild.voice_client
				vc.stop()
				await vc.disconnect()
				info['channel'] = None

			queue = info['queue']
			if queue is not None:
				queue.clear()
				info['queue'] = None

			info['source'] = None

		return True


	@commands.command(
		aliases=['s'],
		help="Skips `index` number of songs, 1 by default"
	)
	@commands.guild_only()
	async def skip(self, ctx: commands.Context, index: int = 1):
		"""
		If the queue is not empty and the client is playing/paused, skips a certain number n of songs.
		In practice, it calls queue.skip(n-1) and stops the current client since the next song will play directly.

		Parameters:
			- index: the number of songs to skip, 1 by default.
		"""

		if index < 1:
			await ctx.send(f"Index can't be lower than 1, try again.")
			return

		guild = ctx.message.guild
		vc = guild.voice_client
		queue: SongQueue = await self.get_queue(ctx)

		if queue is None:
			await ctx.send("The bot is not connected to a voice channel.")

		elif not (vc.is_playing() or vc.is_paused()):
			await ctx.send("Can't skip, no song is currently playing or paused.")

		else:
			try:
				queue.skip(index-1)
				vc.stop()

			except IndexError as ie:
				await ctx.send(f"There's no song with that index, try `{BOT_PREFIX}queue` to see the queue.")

			except Exception as e:
				logger.warning(f"Problem skipping a song, ignoring.")
				logger.debug(f"Unexpected exception:\n{e}")


	@commands.command(
		help="Removes a song from the queue through its `index`, 0 means no song is selected"
	)
	@commands.guild_only()
	async def remove(self, ctx: commands.Context, index: int = 0):
		"""
		Removes a song from the queue if the queue exists and the index is correct.

		Parameters:
			- index: where the song to remove is in the queue. 0 by default,
				this means no song is removed.
		"""

		if index < 1:
			await ctx.send(f"Index can't be lower than 1, try again.")
			return

		try:
			queue = await self.get_queue(ctx)

			if queue is None:
				await ctx.send("The bot is not connected to a voice channel.")

			else:
				status, msg = queue.remove(index)
				dem = {}

				if status:
					dem['title'] = "Removed:"
					dem['description'] = msg
					dem['colour'] = ctx.author.colour
				else:
					dem['title'] = msg
					dem['colour'] = ctx.author.colour

				em = discord.Embed.from_dict(dem)
				await ctx.send(embed=em)

		except IndexError as ie:
			await ctx.send(f"There's no song with that index, try `{BOT_PREFIX}queue` to see the queue.")
		except Exception as e:
			logger.warning(f"Problem removing a song, ignoring.")
			logger.debug(f"Unexpected exception:\n{e}")


	@commands.command(
		aliases=['m'],
		help="Moves a song's position in the queue"
	)
	@commands.guild_only()
	async def move(self, ctx: commands.Context, index1: int, index2: int):
		"""
		Moves the song at index1 to index2 if possible.
		Note: user's list starts at 1, for checks and operations the indexes are given
			as passed by the user.

		Parameters:
			- index1: where the song currently is.
			- index2: where the song is going to be.
		"""

		queue: SongQueue = await self.get_queue(ctx)

		if queue is None:
			pass

		size = queue.get_size()

		if index1 < 1 or index1 > size:
			await ctx.send(f"There's no song with that index! The current queue size is {size}.")
			return

		if index2 < 1 or index2 > size:
			await ctx.send(f"That's out of bounds! The current queue size is {size}.")
			return

		if index1 == index2:
			await ctx.send(f"Left song in place.")

		else:
			res = queue.move(index1, index2)
			if res is not None:
				await ctx.send(res)


	@commands.command(
		aliases=['yt', 'youtube'],
		help="Shows a list of the top 5 results of your search from youtube"
	)
	async def search_youtube(self, ctx: commands.Context, *, search: str):
		"""
		Performs a youtube search and returns the top 5 results.
		Allows the user to easily get more options without having to open youtube when play()'s result isn't satisfying.

		Parameters:
			- search: the query to search for in youtube.
		"""

		search_results: list = ytdl.extract_info(f"ytsearch5:{search}", download=False)['entries']

		async with ctx.typing():
			links = dict()
			order = list()
			for result in search_results:
				url = result['webpage_url']
				tn = result['thumbnail']
				meta = ytdl.extract_info(url, download=False)

				# template: {'title': [url, thumbnail]}
				links[meta['title']] = [url, tn]
				# and add the title to a list to preserve the order
				order.append(meta['title'])

			# Generate the outputs: a first message with the search query,
			# then a message per result with title, url and thumbnail.
			await ctx.send(embed=discord.Embed(title=f"Search results for \"{search}\""))

			cpt = 1
			for title in order:

				tmp = links[title]
				url = tmp[0]
				tn = tmp[1]

				output = f"{cpt}. {title}\n<{url}>\n"

				dem = {
					"description": output,
					"colour": ctx.author.colour
				}

				em = discord.Embed.from_dict(dem)
				em.set_thumbnail(url=tn)

				await ctx.send(embed=em)

				cpt += 1


	@commands.command(
		aliases=['q', 'queue'],
		help="Displays the current queue"
	)
	@commands.guild_only()
	async def show_queue(self, ctx: commands.Context):
		"""
		Displays the current queue as an embed, if it exists.
		"""

		queue: SongQueue = await self.get_queue(ctx)

		if queue is None:
			await ctx.send("The bot is not connected to a voice channel.")

		elif queue.is_empty():
			em = discord.Embed(title="The queue is empty.", colour=ctx.author.color)
			await ctx.send(embed=em)

		else:
			songs = queue.get_songs()

			output = ""
			cpt    = 1
			for song in songs:
				output += f"{cpt}. {song.title}"
				output += "\n"
				cpt += 1

			dem = {
				"title": "Song queue:",
				"description": output,
				"colour": ctx.author.colour
			}
			em = discord.Embed.from_dict(dem)

			await ctx.send(embed=em)


	@commands.command(
		aliases=['vol'],
		help="Changes the volume, range: 0-100"
	)
	@commands.guild_only()
	async def volume(self, ctx: commands.Context, volume: int = -1):
		"""
		Changes the current volume through the source and updates self.info for future sources.

		Parameters:
			- volume: the volume to set, -1 by default to avoid changing it.
				Ranges from 0 to 100.
		"""

		gid = ctx.message.guild.id

		if gid not in self.info:
			await ctx.send("The bot is not connected to a voice channel.")
			return

		source = self.info[gid]['source']

		if volume < 0 or volume > 100:
			em = discord.Embed(title=f"The current volume level is {source.volume*100}%")
			await ctx.send(embed=em)

		else:
			vol = volume/100

			if source is not None:
				source.volume = vol

			self.info[gid]['volume'] = vol

			em = discord.Embed(title=f"Volume level changed to {volume}%")
			await ctx.send(embed=em)


	@commands.command(
		aliases=['now'],
		help="Displays the currently playing song"
	)
	@commands.guild_only()
	async def now_playing(self, ctx: commands.Context):
		"""
		Sends the current song's title and URL as an embed.
		"""

		gid = ctx.message.guild.id

		if gid not in self.info:
			await ctx.send("The bot is not connected to a voice channel.")
			return

		source: YTDLSource = self.info[gid]['source']

		if source is not None:
			output = await source.get_song_info()

			dem = {
				"title": "Now playing:",
				"description": output,
				"colour": ctx.author.color
			}

			em = discord.Embed.from_dict(dem)
			em.set_thumbnail(url=source.thumbnail)

			await ctx.send(embed=em)

		else:
			await ctx.send("The bot is not currently playing something.")


	@commands.command(
		aliases=['mh'],
		help="Moves the bot to your voice channel if the bot's current channel is empty"
	)
	@commands.guild_only()
	async def move_here(self, ctx: commands.Context):
		"""
		Moves the bot to a different channel after checking if the current channel has no human users left.
		"""
		gid = ctx.message.guild.id
		bot_channel = self.info[gid]['channel']
		user_channel = ctx.author.voice.channel

		if bot_channel is None:
			await ctx.send("The bot is not connected to a voice channel.")
			return

		if user_channel is None:
			await ctx.send("You have to be on a voice channel to use this command.")
			return

		if bot_channel.name == user_channel.name:
			await ctx.send("The bot is already on this channel.")
			return

		vc = ctx.message.guild.voice_client
		channel = vc.channel
		members = channel.members

		empty = True
		# We ignore bots, the channel is not empty if there's a non-bot user connected
		for member in members:
			if not member.bot:
				await ctx.send("The bot's current channel is not empty, can't move it.")
				empty = False
				break

		if empty:
			await vc.move_to(user_channel)
			self.info[gid]['channel'] = user_channel
			await ctx.send(f"Moved the bot to {user_channel.name}")


	@commands.group(
		name="favourites",
		aliases=["fav", "favorites"],
		help="Base command for managing your list of favourite songs."
	)
	async def favourites(self, ctx: commands.Context):
		"""
		Base command for managing favourite songs.

		Loads the list of favourites from FAV_LIST_FILE during the first call.
		"""
		global FAV_LIST

		# First verify a subcommand has been used.
		if ctx.invoked_subcommand is None:
			await ctx.send("You have to use a subcommand:")
			await ctx.send_help(self.favourites)
			return

		# Then load the lists if needed.
		if FAV_LIST is None:

			try:
				async with aiofiles.open(FAV_LIST_FILE, 'r') as file:
					content = await file.read()

				if content:
					FAV_LIST = json.loads(content)
				else:
					FAV_LIST = dict()

			except IOError as ioe:
				logger.warning(f"Could not open \"{FAV_LIST_FILE}\", maybe the file doesn't exist: ignoring.")
				logger.debug(f"IOError:\n{ioe}")
				FAV_LIST = dict()

			except Exception as e:
				logger.error(f"Could not load \"{FAV_LIST_FILE}\".")
				logger.debug(f"Unexpected exception:\n{e}")
				await ctx.send("A problem occurred while loading your list, please try again.")
				return

	@favourites.command(
		name="list",
		help="Displays your list of favourites: if an index is specified, shows that song's info"
	)
	async def fav_list(self, ctx: commands.Context, index: int=0):
		"""
		Subcommand to display the list of an user's favourite songs.

		Parameters:
			- index: if less than or equal to zero, it displays the whole list. If greater than zero,
				it displays the song with that index in the list with more info.
		"""
		member: discord.Member = ctx.message.author
		member_id: str = str(member.id)

		songs = FAV_LIST.get(member_id, None)

		if songs is not None:

			if len(songs) == 0:

				name = member.display_name
				if name[-1] == 's':
					title = f"{name}' list"
				else:
					title = f"{name}'s list"

				em = discord.Embed(title=title, description="Your list is empty.")

				await ctx.send(embed=em)
				return

			if index <= 0:

				cpt = 1
				message = ""
				for song in songs:
					message += f"{cpt}. {song.get('title')}\n"
					cpt += 1

				name = member.display_name
				if name[-1] == 's':
					title = f"{name}' list"
				else:
					title = f"{name}'s list"

				em = discord.Embed(
					title=title,
					description=message,
					colour=member.colour
				)

				await ctx.send(embed=em)

			else:

				if index > len(songs):

					await ctx.send(f"There's no song with that index! Your list has {len(songs)} songs.")

				else:

					song = songs[index-1]

					name = member.display_name
					if name[-1] == 's':
						title = f"From {name}' list"
					else:
						title = f"From {name}'s list"

					em = discord.Embed(title=title)
					em.add_field(name="Title", value=song.get('title'), inline=False)
					em.add_field(name="URL", value=song.get('url'))
					em.set_thumbnail(url=song.get('thumbnail'))

					await ctx.send(embed=em)

		else:
			await ctx.send(f"You haven't saved any songs yet, use `{BOT_PREFIX}favourites add <song URL>` or `{BOT_PREFIX}favourites now` to add one.")

	@favourites.command(
		name="add",
		help="Saves a song to your list from its URL"
	)
	async def fav_add(self, ctx: commands.Context, url: str=None):
		"""
		Saves a song to the user's list: uses from_url to get the title and the thumbnail's URL.

		Parameters:
			- url: the URL of the song to save.
		"""
		global FAV_LIST

		if url is None:
			await ctx.send("You have to provide a URL.")
			return

		try:
			# Suppress the embed to avoid clutter.
			msg: discord.Message = ctx.message
			await msg.edit(suppress=True)

			song = await YTDLSource.from_url(url, download=False)
			info = dict()
			info['title'] = song.title
			info['url'] = song.url
			info['thumbnail'] = song.thumbnail

			member: discord.Member = ctx.message.author
			member_id: str = str(member.id)

			songs = FAV_LIST.get(member_id, None)

			if songs is not None:
				songs.append(info)
			else:
				songs = [info]
				FAV_LIST[member_id] = songs

			dump = json.dumps(FAV_LIST)
			async with aiofiles.open(FAV_LIST_FILE, 'w') as file:
				await file.write(dump)

			em = discord.Embed(description=f"Added \"{info.get('title')}\" to your list.")

			await ctx.send(embed=em)

		except MaxDurationError:
			await ctx.send("The song is too long to be played, so it can't be saved.")

		except Exception as e:
			logger.error("Could not add a song to list of favourites.")
			logger.debug(f"Exception:\n{e}")
			await ctx.send("An error occurred while saving the song, please try again.")

	@favourites.command(
		name="remove",
		help="Removes a song from your list by its index, 0 means no song is removed"
	)
	async def fav_remove(self, ctx: commands.Context, index: int=0):
		"""
		Remove a song from the user's list by its index.

		Parameters:
			- index: the index of the song to remove, 0 by default to avoid removing anything.
		"""
		global FAV_LIST

		if index <= 0:
			await ctx.send(f"You have to select a valid index. Use `{BOT_PREFIX}favourites list` to check your list.")
			return

		member_id: str = str(ctx.message.author.id)
		songs: List[Dict[str, str]] = FAV_LIST.get(member_id, None)

		if songs is None:
			await ctx.send(f"You haven't saved any songs yet.")
			return

		if index > len(songs):
			await ctx.send(f"You have to select a valid index: there's only {len(songs)} songs in your list.")
			return

		song = songs.pop(index-1)

		try:
			dump = json.dumps(FAV_LIST)
			async with aiofiles.open(FAV_LIST_FILE, 'w') as file:
				await file.write(dump)

			message = f"Removed \"{song.get('title')}\" from your list."
			em = discord.Embed(description=message)
			await ctx.send(embed=em)

		except Exception as e:
			logger.error("Couldn't save favourites list after removing a song.")
			logger.debug(f"Exception:\n{e}")

	@favourites.command(
		name="now",
		help="Saves the currently playing song to your list"
	)
	@commands.guild_only()
	async def fav_now(self, ctx: commands.Context):
		"""
		Saves the currently playing song from self.info.source.
		"""
		global FAV_LIST

		gid = ctx.message.guild.id

		if gid not in self.info:
			await ctx.send("The bot is not connected to a voice channel.")
			return

		info = self.info.get(gid)
		source: YTDLSource = info.get('source')

		if source is not None:
			
			member_id: str = str(ctx.message.author.id)

			songs = FAV_LIST.get(member_id, None)

			song = dict()
			song['title'] = source.title
			song['url'] = source.url
			song['thumbnail'] = source.thumbnail

			if songs is not None:
				songs.append(song)
			else:
				songs = [song]
				FAV_LIST[member_id] = songs

			try:
				dump = json.dumps(FAV_LIST)
				async with aiofiles.open(FAV_LIST_FILE, 'w') as file:
					await file.write(dump)

				em = discord.Embed(description=f"Added \"{song.get('title')}\"to your list.")

				await ctx.send(embed=em)

			except Exception as e:
				logger.error("Could not save a song to FAV_LIST_FILE.")
				logger.debug(f"Exception:\n{e}")
				await ctx.send("An error occurred while saving the song, please try again.")

		else:

			await ctx.send(f"The bot is not playing something at the moment, try `{BOT_PREFIX}play <song>`.")

	@favourites.command(
		name="play",
		help="Plays a song from your list by its index"
	)
	@commands.guild_only()
	async def fav_play(self, ctx: commands.Context, index: int=0):
		"""
		Play a song from the user's list by passing its URL to self.play.

		Parameters:
			- index: the index of the song to play, 0 by default.
		"""

		if index <= 0:
			await ctx.send("You have to provide a valid index.")
			return

		member_id: str = str(ctx.message.author.id)
		songs = FAV_LIST.get(member_id, None)

		if songs is None:
			await ctx.send(f"You haven't saved a song yet, you cas use `{BOT_PREFIX}favourites add <URL>` or `{BOT_PREFIX}favourites now`.")
			return

		if index > len(songs):
			await ctx.send(f"You have to provide a valid index, your list only has {len(songs)} songs.")
			return

		song = songs[index-1]

		url = song.get('url')
		await self.play(ctx, url)


	@commands.Cog.listener('on_voice_state_update')
	async def on_empty_channel(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
		"""
		Disconnects the bot if no (non-bot) users are left in the channel.
		"""
		vc = member.guild.voice_client

		if vc is not None:

			members = vc.channel.members
			empty = True

			for member in members:
				if not member.bot:
					empty = False
					break

			if empty:
				# I don't know if there's a way to get the context, so manual stopping,
				# clearing queue and leaving it is
				if vc.is_connected():

					gid = member.guild.id
					queue = self.info[gid]['queue']
					channel = self.info[gid]['channel']

					vc.stop()
					queue.clear()

					self.info[gid]['queue'] = None
					self.info[gid]['channel'] = None

					await vc.disconnect()
					vc.cleanup()
					logger.debug(f"{VOICE} Left \"{channel}\"")



class MaxDurationError(Exception):
	"""Raised when video length is greater than MAX_DURATION."""
	pass


class YTDLSource(discord.PCMVolumeTransformer):

	def __init__(self, source, *, song, volume=0.5):
		super().__init__(source, volume)
		self.song: Song = song
		self.title: str = song.title
		self.file: str  = song.file
		self.url: str   = song.url
		self.thumbnail: str  = song.thumbnail

	@classmethod
	async def from_url(cls, url: str, *, loop: asyncio.AbstractEventLoop=None, download: bool=True) -> Song:
		"""
		Downloads a song from its URL.

		Parameters:
			- url: the url to download from.
			- loop: the EventLoop to use.
			- download: whether the song should be downloaded.
		Returns:
			- The corresponding (new) Song instance.
		"""

		loop = loop or asyncio.get_event_loop()

		metadata = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

		duration = metadata['duration']
		if duration > MAX_DURATION:
			logger.warning(f"Video is too long. MAX_DURATION={MAX_DURATION}")
			logger.debug(f"Title: {metadata['title']}")
			logger.debug(f"URL: {url}")
			raise MaxDurationError

		# Check if the video is already saved:
		# Get the first entry
		if 'entries' in metadata:
			metadata = metadata['entries'][0]
		# Get the filename
		filename = ytdl.prepare_filename(metadata)

		# If it isn't already there, download it
		if download and not os.path.exists(filename):
			await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=True))

		song = Song(metadata['title'], filename, url, metadata['thumbnail'])
		return song

	async def get_song_info(self) -> str:
		"""
		Returns:
			- A string containing the source's song title and URL.
		"""
		return f"{self.song.title} - {self.song.url}"


async def validate_url(url: str) -> bool:
	"""
	Checks to see if url has any valid extractors for youtube_dl

	Parameters:
		- url: the url to search for extractors.

	Returns:
		- True, if site has dedicated extractor
		- False, if site has no dedicated extractor

	"""
	e = youtube_dl.extractor.get_info_extractor('Youtube')
	return e.suitable(url)


def setup(bot):
	global logger
	logger = logging.getLogger("CroissantBot")
	bot.add_cog(Music(bot))
