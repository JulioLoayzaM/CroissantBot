# meme.py
#
# Cog to get the 'hottest' posts from a subreddit and download
# the first (meme) image post to send it.
# Keeps track of downloaded memes per server to avoid sending duplicates.


# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


import aiofiles
import aiohttp
import asyncpraw
import logging
import discord
import os

from dotenv import load_dotenv, set_key
from typing import Union

from discord.ext import commands


class Meme(commands.Cog):

	def __init__(
		self,
		bot: commands.Bot,
		logger: logging.Logger,
		session: aiohttp.ClientSession,
		reddit: asyncpraw.Reddit,
		meme_dir: str,
		download: bool,
		item_limit: int
	):
		self.bot = bot
		self.logger = logger
		self.session = session
		self.reddit = reddit
		self.dir = meme_dir
		self.download = download
		self.item_limit = item_limit

	async def close_session(self) -> bool:
		"""
		Closes the aiohttp.session and the Reddit instance, called on bot exit.

		Returns:
			True if the sessions were closed, False otherwise.
		"""

		try:
			await self.session.close()
			await self.reddit.close()
			return True
		except Exception as error:
			self.logger.error("Couldn't close a Meme cog session.")
			self.logger.debug(error)
			return False

	async def get_meme(self, sub: str, name: str) -> Union[str, None]:
		"""
		Downloads a meme from a given subreddit and returns the path to the downloaded file.

		Parameters:
			sub: The subreddit from which memes are taken.
			name: Either the guild's name or the private channel's ID. This allows to
			a list of already sent memes for each one.

		Returns:
			The path to the file if the meme was successfully/already downloaded,
			string 'Empty' if it couldn't find new posts on the selected subreddit or
			None if the meme couldn't be downloaded.
		"""

		DOWNLOAD = self.download
		ITEM_LIMIT = self.item_limit
		MEME_DIR = self.dir

		logger = self.logger
		reddit = self.reddit

		# File to check to see if the meme was already sent to this guild/DM
		list_file = f"{MEME_DIR}/{name}.txt"

		subreddit = await reddit.subreddit(sub, fetch=True)

		# Returning Empty means there are no new posts in this subreddit
		# to send to this guild/DM.
		filename = "Empty"

		async for meme in subreddit.hot(limit=ITEM_LIMIT):

			url: str = meme.url

			# is_self means the post is text-only.
			# We also want images or gifs, not videos.
			# Finally, stickied posts may be mods', we assume those aren't memes.
			if meme.is_self or meme.is_video or meme.stickied:
				continue

			# Get the filename, the same one as on the link.
			# For example: https://i.redd.it/thisisnotameme.jpg
			temp = url.split('/')

			# This results in: thisisnotameme.jpg
			meme_file = temp[-1]

			try:
				new = True

				# Using 'a+' because we don't want to truncate the file if it exists.
				async with aiofiles.open(list_file, 'a+') as file:
					await file.seek(0)
					# We check the list to see if this meme was already sent to this guild
					async for line in file:
						line = line.rstrip('\n')
						if line == meme_file:
							new = False
							break

					# If the meme is not on the list, add it
					if new:
						# Go to end to append filename
						await file.seek(0, 2)
						await file.write(f"{meme_file}\n")

					# If the meme is on the list, skip to next
					else:
						continue

			except IOError as ioe:

				logger.warning(f"Couldn't check is meme is already in {list_file}.")
				logger.debug(f"IOError:\n{ioe}")
				logger.warning("Ignoring error, proceeding.")

			if not DOWNLOAD:
				return url

			# We need to add the path of the memes' directory
			filename = f"{MEME_DIR}/{meme_file}"

			# With the complete path, we can check if the meme was already downloaded
			# since it could have been sent to another guild in the meantime.
			if os.path.exists(filename):
				# If the file is already there, there's nothing to download.
				break

			# If not, we download it.
			else:

				try:

					async with self.session.get(url) as response:
						if response.status == 200:
							async with aiofiles.open(filename, mode='wb') as img_file:
								await img_file.write(await response.read())
						else:
							logger.warning("Error while getting meme.")
							logger.debug(f"Received status {response.status}, reason: {response.reason}")
							continue

					logger.debug(f"{meme_file} downloaded.")

					# We break to return the filename.
					break

				except Exception as e:

					logger.error("Could not write image file.")
					logger.debug(f"Unexpected exception:\n{e}")
					# Return None to indicate there's been a problem during download.
					return None

		return filename

	@commands.command(
		name="meme",
		help="Sends meme from subreddit, r/memes by default"
	)
	async def send_meme(self, ctx: commands.Context, sub: str = "memes"):
		"""
		Sends a meme returned by get_meme.

		Parameters:
			sub: The subreddit to get the meme from, 'memes' by default.
		"""

		chtype = str(ctx.channel.type)
		DOWNLOAD = self.download
		logger = self.logger

		if chtype == "text":
			name = ctx.guild.name
		elif chtype == "private":
			name = str(ctx.channel.id)
		else:
			logger.error(f"chtype is not text or private: {chtype}")
			await ctx.send("An error occurred, please try again.")
			return

		async with ctx.typing():
			output = await self.get_meme(sub, name)

		if output is None:
			await ctx.send("An error occurred, please try again.")

		elif output == "Empty":
			await ctx.send(f"No new recent posts from r/{sub}, try another sub.")

		else:
			try:
				if not DOWNLOAD:
					em = discord.Embed()
					em.set_image(url=output)
					await ctx.send(embed=em)
				else:
					await ctx.send(file=discord.File(output))

			except discord.HTTPException as he:
				logger.error(f"{output} is too big to send")
				logger.debug(f"discord.HTTPException:\n{he}")
				await ctx.send("The meme was too big to send, please try again.")

			except Exception as e:
				logger.error("Couldn't send meme")
				logger.debug(f"Unexpected exception:\n{e}")
				logger.debug(f"Output:\n{output}")
				await ctx.send("An error ocurred, please try again.")

	@commands.command(
		name="change_meme_limit",
		help="Change the limit of memes the bot can get at each call from a subreddit"
	)
	@commands.is_owner()
	async def change_limit(
		self,
		ctx: commands.Context,
		new_limit: int
	):
		"""
		Changes the item_limit of memes the bot can get from a subreddit on each request.

		Parameters:
			new_limit: The new limit to apply. Has to be a strictly positive integer.
		"""
		if new_limit > 0:

			self.item_limit = new_limit

			try:
				set_key('.env', 'MEME_ITEM_LIMIT', str(new_limit))
				em = discord.Embed(
					title="Success",
					description=f"Changed limit to {new_limit}.",
					colour=discord.Colour.green()
				)
				await ctx.send(embed=em)
				self.logger.debug("Updated MEME_ITEM_LIMIT.")

			except Exception as error:
				self.logger.error("Couldn't set new_limit in .env.")
				self.logger.debug(error)
				em = discord.Embed(
					title="Error",
					description="""
						The new limit was applied to the current session, but couldn't be saved
						in `.env`.
					""",
					colour=discord.Colour.gold()
				)
				await ctx.send(embed=em)

		else:
			em = discord.Embed(
				title="Error",
				description="Can't set the limit below 0.",
				colour=discord.Colour.gold()
			)
			await ctx.send(embed=em)


def setup(bot):

	WARNING   = '\033[93m'
	ENDC      = '\033[0m'

	load_dotenv()

	logger = logging.getLogger("CroissantBot")

	session = aiohttp.ClientSession()
	logger.debug(f"{WARNING}Created:{ENDC} Meme aiohttp.ClientSession.")

	CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID")
	CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
	USERNAME      = os.getenv("REDDIT_USERNAME")
	PASSWORD      = os.getenv("REDDIT_PASSWORD")
	APP_VERSION   = os.getenv("REDDIT_APP_VERSION")

	reddit = asyncpraw.Reddit(
		client_id     = CLIENT_ID,
		client_secret = CLIENT_SECRET,
		username      = USERNAME,
		password      = PASSWORD,
		user_agent    = f"python/requests:{CLIENT_ID}:v{APP_VERSION} (by /u/{USERNAME})"
	)

	# Directory containing the lists (and the memes if download is enabled).
	# "./memes" by default - "." is the directory contaning bot.py.
	meme_dir = os.getenv("MEME_DIR")

	# Whether to download the memes or not, False by default.
	download = bool(os.getenv('MEME_DOWNLOAD', False))
	status = "ON" if download else "OFF"
	logger.debug(f"{WARNING}Meme download:{ENDC} {status}.")

	# The number of memes the bot will fetch when called.
	# AFAIK, we can only set how many items to fetch, meaning each time
	# the function is called with the same sub we may get the same exact list,
	# just to get the next meme. If the command is used often, the limit
	# should be increased or a better way to fetch memes implemented.
	item_limit = int(os.getenv('MEME_ITEM_LIMIT', 10))

	bot.add_cog(
		Meme(
			bot,
			logger,
			session,
			reddit,
			meme_dir,
			download,
			item_limit
		)
	)
