# misc.py
#
# Cog for miscellaneous commands, such as kill or croissant.


# Copyright (C) 2021 Julio Loayza
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


import random
import json
import logging
import os

import discord
from discord.ext import commands

from dotenv import load_dotenv


load_dotenv()
# kill - phrases text file
KILL_MESSAGES_FILE = os.getenv("KILL_PATH")
# kill - count json file
KILL_COUNT_FILE    = os.getenv("KILL_COUNT")
# croissant.gif path
CROISSANT_PATH     = os.getenv("CROISSANT_PATH")

# kill - kill count
kill_count = dict()
# kill - suicide count
suicide_count = dict()

# 'CroissantBot' logger
logger = None

class Misc(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.command(
		name="add",
		help="Adds two integers"
	)
	async def add_two(self, ctx: commands.Context, num1: int, num2: int):
		"""
		Adds two integers, with some easter eggs.
		Simple example of Converters: they cast num1/num2 to int
		and throw an error if unsuccessful.
		"""
		if (num1 == 2) and (num2 == 2):
			r = random.randint(1,3)
			if r == 1:
				await ctx.send(":fish:")
			elif r == 2:
				await ctx.send("5")
			else:
				await ctx.send("4")
		else:
			result = num1 + num2
			if result == 42:
				await ctx.send("42, the answer to the ultimate question of life, the universe, and everything")
			else:
				await ctx.send(num1 + num2)

	@add_two.error
	async def add_two_error(self, ctx: commands.Context, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("`add` takes two integers as arguments.")


	@commands.command()
	@commands.guild_only()
	async def poggers(self, ctx: commands.Context):
		"""
		Responds with a poggers emote, if available.
		"""
		guild: discord.Guild = ctx.guild

		emojis = await guild.fetch_emojis()

		for emoji in emojis:
			
			if emoji.name == "poggers":

				await ctx.send(emoji)
				return

		await ctx.send("This server doesn't have a poggers emote")


	@commands.command(
		help="🥐"
	)
	async def croissant(self, ctx: commands.Context):
		"""
		Croissant - sends a gif.
		"""
		await ctx.send(file=discord.File(CROISSANT_PATH))


	@commands.command(
		help="Kill your enemies (and your friends)"
	)
	@commands.guild_only()
	async def kill(self, ctx: commands.Context, member: discord.Member = None):
		"""
		Sends a random phrase if a user is selected. If the calling user is selected, sends a (hardcoded) suicide message.
		Tracks how many times someone has killed a specific member or themselves in the current guild.
		The format used for the kill_count file is:
		{
			'guild_id': {
				'killer_id': {
					'victim_id': count
				}
			}
		}
		Note: guild_id, killer_id and victim_id are strings.
		For suicide_count, the {victim_id:count} pair is replaced by the suicide count.
		"""

		global kill_count

		if member is None:
			await ctx.send("You have to select a victim! :slight_smile:")

		else:
			check = ctx.guild.get_member(member.id)

			if check is None:
				await ctx.send("That user is not in this server.")

			else:
				killer: str = str(ctx.author.id)
				victim: str = str(member.id)

				gid: str = str(ctx.guild.id)

				# If they are the same, update suicide count
				if killer == victim:

					if gid not in suicide_count:
						suicide_count[gid] = dict()

					# Get the count for this guild
					current_count = suicide_count[gid]

					if killer not in current_count:
						current_count[killer] = 1
					else:
						current_count[killer] += 1

					# Choose a message depending on how many times the user killed themselves
					if current_count[killer] < 3:
						await ctx.send("Great, you killed yourself.")
					elif current_count[killer] < 6:
						await ctx.send("You ok?")
					elif current_count[killer] < 9:
						await ctx.send("Uh...")
					else:
						await ctx.send("I'm going to stop counting...")

				# If not the same ID, pick a phrase from the file and send it
				else:
					killer_name: str = ctx.author.display_name
					victim_name: str = member.display_name
					try:
						# We first try to read the file then update the kill count to avoid registering
						# the kill in case of failure
						# MAYBE: add more try-catch statements to separate the different IOErrors possible

						with open(KILL_MESSAGES_FILE, 'r') as file:
							lines = file.readlines()

						line = random.choice(lines)
						line = line.rstrip('\n')
						line = line.replace("<killer>", killer_name)
						line = line.replace("<victim>", victim_name)
						await ctx.send(line)

						# If kill_count is empty we load the json copy, which may be empty as well
						if not kill_count:
							with open(KILL_COUNT_FILE, 'r') as f:
								kill_count = json.load(f)

						if gid not in kill_count:
							kill_count[gid] = dict()

						# Get the count for this guild
						current_count = kill_count[gid]

						# If killer is not in current_count, we create its victims dict and add the current victim
						if killer not in current_count:
							tmp = dict()
							tmp[victim] = 1
							current_count[killer] = tmp

						else:
							killer_count = current_count[killer]
							if victim not in killer_count:
								killer_count[victim] = 1
							else:
								killer_count[victim] += 1

						# Save the new count to the file
						with open(KILL_COUNT_FILE, 'w') as f:
							json.dump(kill_count, f)

					except IOError as ie:
						logger.error(f"Error while updating count.")
						logger.debug(f"IOError:\n{ie}")

					except Exception as e:
						logger.error(f"Error while updating count.")
						logger.debug(f"Unexpected exception:\n{e}")


	@commands.command(
		aliases=['count', 'kc'],
		help="Shows your kill count, can specify a user to check your stats against them"
	)
	@commands.guild_only()
	async def kill_count(self, ctx: commands.Context, member: discord.Member = None):
		"""
		Checks kill_count (and loads from json if necessary) then sends stats for calling user.
		Can pass a member as argument to check stats against that member.
		"""

		global kill_count

		# Check is kill_count is empty, load from the json if it's the case
		if not kill_count:
			try:
				with open(KILL_COUNT_FILE, 'r') as f:
					kill_count = json.load(f)
			except IOError as ie:
				logger.error(f"Couldn't read {KILL_COUNT_FILE}")
				logger.debug(f"IOError:\n{ie}")
				await ctx.send("Error fetching the count, please try again.")
			except Exception as e:
				logger.error(f"Couldn't read {KILL_COUNT_FILE}")
				logger.debug(f"Unexpected exception:\n{e}")
				await ctx.send("Error fetching the count, please try again.")

		killer_name: str = ctx.author.display_name
		killer_id: str = str(ctx.author.id)

		if member is not None:
			victim_name: str = member.display_name
			victim_id: str = str(member.id)

		# Get the guild id as str and the guild count
		gid = str(ctx.guild.id)
		if gid not in kill_count:
			kill_count[gid] = dict()

		current_count = kill_count[gid]

		if killer_id not in current_count:
			await ctx.send("You haven't killed anyone... yet :slight_smile:")

		else:
			kname_count = current_count[killer_id]

			# If no member is passed, display the general count
			if member is None:

				if killer_name[-1].lower() == 's':
					title = f"{killer_name}' count"
				else:
					title = f"{killer_name}'s count"

				em = discord.Embed(title=title, colour=ctx.author.colour)

				for victim_id in kname_count:
					victim: discord.Member = ctx.guild.get_member(int(victim_id))
					if victim is not None:
						victim_name: str = victim.display_name
						em.add_field(name=victim_name, value=kname_count[victim_id], inline=True)

			# Else show the count against the specified user
			else:
				em = discord.Embed(title=killer_name, description=f"You've killed **{victim_name}** {kname_count[victim_id]} times.", colour=ctx.author.colour)

			await ctx.send(embed=em)



def setup(bot):
	global logger
	logger = logging.getLogger("CroissantBot")
	bot.add_cog(Misc(bot))