# db.py
#
# Defines a class, which represents a connection to a PostgreSQL database,
# used to manage the playlists.

import asyncio
import asyncpg
import logging

from .song import Song

# from dotenv import load_dotenv
# from os import getenv
# from typing import Union


# Colours for logs.
GREEN = '\033[92m'
WARNING = '\033[93m'
CYAN = '\033[96m'
ENDC = '\033[0m'
RED = '\033[91m'
FAIL = RED


class DatabaseConnection():
	"""
	A class to represent a connection to the PostgreSQL database.

	:param logger_name:
		The name of the logger to be used by the connection.
	:type logger_name: str
	"""

	def __init__(self, logger_name: str):
		"""
		init

		:param logger_name:
			The name of the logger to be used by the connection.
		:type logger_name: str
		"""
		self.conn = None
		self.logger = logging.getLogger(logger_name)

	async def connect(
		self,
		host: str,
		user: str,
		password: str,
		database: str,
		loop: asyncio.AbstractEventLoop = None,
		port: str = None
	) -> asyncpg.Connection:
		"""
		Connect to a database using the credentials provided. Stores connection in self.conn.

		:param host:
			The hostname, usually 'localhost'.
		:type host: str

		:param user:
			A user with access to the database.
		:type user: str

		:param password:
			The user's password.
		:type password: str

		:param database:
			The name of the database to connect to.
		:type database: str

		:param loop:
			The `asyncio` loop to use. If None, `asyncpg` uses the default event loop.
			None by default.
		:type loop: asyncio.AbstractEventLoop

		:param port:
			The port to use, usually 5432. None by default.
		:type port: str
		"""

		conn = await asyncpg.connect(
			host=host, port=port, user=user, password=password, database=database, loop=loop
		)

		self.conn = conn

		self.logger.debug(f"{GREEN}Connected to database:{ENDC} {database}.")

	async def close(self) -> bool:
		"""
		Closes the connection to the database.

		:returns: True if the connection was closed, False if there was no connection to close.
		:rtype: bool
		"""

		if self.conn is not None:
			await self.conn.close()
			self.logger.debug(f"{WARNING}Closed connection to the database.{ENDC}")
			return True

		else:
			self.logger.warning("No database connection to close.")
			return False

	async def insert_song(
		self,
		song: Song
	) -> bool:
		"""
		Inserts a song in the database.

		:param song:
			The song to insert.
		:type song: Song

		:returns True if the song was successfully inserted, False otherwise:
		:rtype bool:
		"""

		query = """
			INSERT INTO songs(song_id, title, url, thumbnail)
			VALUES (NEXTVAL('songs_song_id_seq'), $1, $2, $3);
		"""
		values = (song.title, song.url, song.thumbnail)

		res = await self.conn.execute(query, *values)

		return res == "INSERT 0 1"
