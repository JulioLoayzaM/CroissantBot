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


import asyncio
import aiofiles
import aiohttp
import asyncpraw
import logging
import discord
import os

from dotenv import load_dotenv
from typing import Union

from discord.ext import commands


# .env variables
load_dotenv()
CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USERNAME      = os.getenv("REDDIT_USERNAME")
PASSWORD      = os.getenv("REDDIT_PASSWORD")
APP_VERSION   = os.getenv("REDDIT_APP_VERSION")

# Directory containing the memes and lists
# "./memes" by default - "." is the directory contaning bot.py
MEME_DIR = os.getenv("MEME_DIR")

# The number of memes the bot will fetch when called.
# AFAIK, we can only set how many items to fetch, meaning each time
# the function is called with the same sub we may get the same exact list,
# just to get the next meme. If the command is used often, the limit
# should be increased or a better way to fetch memes implemented.
item_limit = 10

# The 'CroissantBot' logger
logger = None

class Meme(commands.Cog):
	
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	async def get_meme(self, sub: str, name: str) -> Union[str, None]:
		"""
		Downloads a meme from a given subreddit and returns the path to the downloaded file.
		'name' is either the guild's name or the private channel's ID. This allows to keep a list of
		already sent memes for each one.
		"""

		reddit = asyncpraw.Reddit(
			client_id     = CLIENT_ID, 
			client_secret = CLIENT_SECRET, 
			username      = USERNAME,
			password      = PASSWORD,
			user_agent    = f"python/requests:{CLIENT_ID}:v{APP_VERSION} (by /u/{USERNAME})"
		)

		# File to check to see if the meme was already sent to this guild/DM
		list_file = f"{MEME_DIR}/{name}.txt"

		subreddit = await reddit.subreddit(sub, fetch=True)

		# Returning Empty means there are no new posts in this subreddit
		# to send to this guild/DM.
		filename = "Empty"

		async for meme in subreddit.hot(limit=item_limit):

			url = meme.url

			# is_self means the post is text-only.
			# We also want images or gifs, not videos.
			# Finally, stickied posts may be mods', we assume those aren't memes.
			if meme.is_self or meme.is_video or meme.stickied:
				continue

			try:
				new = True

				# Use 'a+' because with aiofiles 'w+' can't read the file
				async with aiofiles.open(list_file, 'a+') as file:
					await file.seek(0)
					# We check the list to see if this meme was already sent to this guild
					async for line in file:
						line = line.rstrip('\n')
						if line == url:
							new = False
							break

					# If the meme is not on the list, add it
					if new:
						# Go to end to append filename
						await file.seek(0, 2)
						await file.write(f"{url}\n")

					# If the meme is on the list, skip to next
					else:
						continue

			except IOError as ioe:

				logger.warning(f"Couldn't check is meme is already in {list_file}.")
				logger.debug(f"IOError:\n{ioe}")
				logger.warning("Ignoring error, proceeding.")

			# Get the filename, the same one as on the link.
			# For example: https://i.redd.it/thisisnotameme.jpg
			temp = url.split('/')

			# This results in: thisisnotameme.jpg
			meme_file = temp[-1]

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

					async with aiohttp.ClientSession() as session:
						async with session.get(url) as response:
							if response.status == 200:
								async with aiofiles.open(filename, mode='wb') as img_file:
									await img_file.write(await response.read())
							else:
								logger.warning(f"Error while getting meme.")
								logger.debug(f"Received status {response.status}, reason: {response.reason}")
								continue

					logger.debug(f"{meme_file} downloaded.")

					# We break to return the filename.
					break

				except Exception as e:

					logger.error(f"Could not write image file.")
					logger.debug(f"Unexpected exception:\n{e}")
					# Return None to indicate there's been a problem during download,
					# close the instance before leaving.
					await reddit.close()
					return None

		await reddit.close()

		return filename


	@commands.command(
		name="meme",
		help="Sends meme from subreddit, r/memes by default"
	)
	async def send_meme(self, ctx: commands.Context, sub: str="memes"):
		"""
		Sends a meme returned by get_meme.
		"""

		chtype = str(ctx.channel.type)

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
				await ctx.send(file=discord.File(output))

			except discord.HTTPException as he:
				logger.error(f"{output} is too big to send")
				logger.debug(f"discord.HTTPException:\n{he}")
				await ctx.send("The meme was too big to send, please try again.")

			except Exception as e:
				logger.error(f"Couldn't send meme")
				logger.debug(f"Unexpected exception:\n{e}")
				logger.debug(f"Output:\n{output}")
				await ctx.send("An error ocurred, please try again.")



def setup(bot):
	global logger
	logger = logging.getLogger("CroissantBot")
	bot.add_cog(Meme(bot))