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


import youtube_dl
import asyncio
import logging
import os

import discord
from discord.ext import commands

from cogs.queue import SongQueue
from cogs.song import Song

from dotenv import load_dotenv
from typing import Tuple


# Colours and string for some coloured output
BLUE = '\033[94m'
ENDC = '\033[0m'
VOICE = f"{BLUE}[voice]{ENDC}"


load_dotenv()
# Videos longer than MAX_DURATION seconds won't be downloaded
MAX_DURATION = int(os.getenv('MAX_DURATION'))
# Directory in which music is downloaded
SAVE_DIR = os.getenv('MUSIC_DIR')

BOT_PREFIX = os.getenv('BOT_PREFIX')

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


	@commands.command(
		aliases=['p'],
		help="Plays first search result from youtube. For URLs, use `play_from`"
	)
	@commands.guild_only()
	async def play(self, ctx: commands.Context, *, query: str):
		"""
		This function searches youtube and passes the first result URL to play_from,
		which handles the creation of a Song and its queueing.
		"""

		# to use search instead of passing an url, prepend 'ytsearch:' to the search terms
		# to search for more than one video, prepend 'ytsearchx:' with x being the number of videos
		video = ytdl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
		url = video['webpage_url']

		await self.play_from(ctx, url)


	async def get_queue(self, ctx: commands.Context):
		"""
		Returns the corresponding queue, None if not connected to a voice channel in the context's guild.
		"""
		guild_id = ctx.message.guild.id

		# Return None if the guild is not in info, meaning the bot is not connected
		# to a voice channel in that guild
		if guild_id not in self.info:
			return None

		queue = self.info[guild_id]['queue']
		return queue


	@commands.command(
		aliases=['pf'],
		help=f"Plays a song from an URL. Use `{BOT_PREFIX}search_youtube <query>` to get a list of related links"
	)
	@commands.guild_only()
	async def play_from(self, ctx: commands.Context, url: str = None):
		"""
		This function is in charge of downloading the audio, creating the Song instance and queueing the song.
		Additionally, if no song is playing it calls play_song() to start streaming.
		"""

		if url is None:
			await ctx.send(f"You have to provide a youtube url. Use `{BOT_PREFIX}play <query>` to search and play from youtube directly.")
		
		else:

			# To avoid clutter, we edit the user's message to suppress the embed
			msg = ctx.message
			await msg.edit(suppress=True)

			try :
				guild = ctx.message.guild
				vc = guild.voice_client

				queue = await self.get_queue(ctx)

				if queue is None:
					await ctx.send("The bot is not connected to a voice channel.")
					return

				# MAYBE: from_url should return a Song directly
				filename, title, thumbnail = await YTDLSource.from_url(url, loop=self.bot.loop)

				# Create an instance of Song
				song = Song(title, filename, url, thumbnail)

				queue.push(song)

				# If a song is playing or paused but not stopped, send a message
				# to indicate the song is queued
				if vc.is_playing() or vc.is_paused():
					dem = {
						"title": "Queued:",
						"description": f"{title} - <{url}>",
						"colour": ctx.author.color
					}
					em = discord.Embed.from_dict(dem)
					em.set_thumbnail(url=thumbnail)
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


	async def play_song(self, ctx: commands.Context):
		"""
		Function in charge of actually playing a song.
		It assumes three things:
			- the songs in the queue are already downloaded
			- if a song is playing and we called play_song anyway, we want to skip the song
			- the bot is actually connected to a voice channel
		"""

		guild = ctx.message.guild
		vc: discord.VoiceClient = guild.voice_client

		def play_next():

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
				return f"The queue is empty, use `{BOT_PREFIX}play` or `{BOT_PREFIX}play_from` to start playing music.", None

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
				await ctx.send(f"The bot is not currently playing something, try `{BOT_PREFIX}play` or `{BOT_PREFIX}play_from`.")

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
	async def from_url(cls, url: str, *, loop=None) -> Tuple[str]:
		"""
		Downloads a song from its URL.

		Returns:
			- The downloaded file's path
			- The title of the video
			- The thumbnail's address
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
		if not os.path.exists(filename):
			await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=True))

		return filename, metadata['title'], metadata['thumbnail']

	async def get_song_info(self) -> str:
		"""
		Returns:
			- A string containing the source's song title and URL.
		"""
		return f"{self.song.title} - {self.song.url}"


def setup(bot):
	global logger
	logger = logging.getLogger("CroissantBot")
	bot.add_cog(Music(bot))