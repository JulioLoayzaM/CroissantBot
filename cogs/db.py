# db.py
#
# Defines a class, which represents a connection to a PostgreSQL database,
# used to manage the playlists.

import asyncio
import asyncpg
import logging

from .song import Song
from typing import List, Union


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

		:return:
			True if the connection was closed, False if there was no connection to close.
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
	):
		"""
		Inserts a song in the database.

		:param song:
			The song to insert.
		:type song: Song

		:raises DbInsertError:
			Raised when an error inserting a song occurs.
		"""

		query = """
			INSERT INTO songs(song_id, title, url, thumbnail)
			VALUES (NEXTVAL('songs_song_id_seq'), $1, $2, $3);
		"""
		values = (song.title, song.url, song.thumbnail)

		try:
			await self.conn.execute(query, *values)
		except Exception as error:
			self.logger.debug(error)
			raise DbInsertError("Could not insert a song.", values)

	async def get_song_id(
		self,
		song: Song
	) -> Union[int, None]:
		"""
		Get the database ID of a song.

		:param song:
			The song to search for.
		:type song: Song

		:return:
			The ID of the song if it exists, None otherwise.
		:rtype: Union[int, None]
		"""

		query = """
			SELECT song_id
			FROM songs
			WHERE url = $1;
		"""

		song_id: Union[int, None] = await self.conn.fetchval(query, song.url)

		return song_id

	async def song_exists(
		self,
		song: Song
	) -> bool:
		"""
		Check if a song exists in the database.

		:param song:
			The song to search for.
		:type song: Song

		:return:
			True if the song exists, False otherwise.
		:rtype: bool
		"""

		song_id: Union[int, None] = await self.get_song_id(song)

		if song_id is None:
			return False

		# TODO: check if title and thumbnail are up to date.
		return True

	async def song_matches_playlist(
		self,
		song: Song,
		playlist_title: str,
		owner_id: str
	) -> bool:
		"""
		Check if a song is matched to a playlist in songs_in_lists.

		:param song:
			The song to check.
		:type song: Song

		:param playlist_title:
			The title of the playlist to check.
		:type playlist: str

		:param owner_id:
			The owner of the playlist to check.
		:type owner_id: str

		:return:
			True if the song and the playlist are matched, False otherwise.
		:rtype: bool
		"""

		song_id = await self.get_song_id(song)
		if song_id is None:
			return False

		playlist_id = await self.get_playlist_id(playlist_title, owner_id)
		if playlist_id is None:
			return False

		query = """
			SELECT exists(
				SELECT *
				FROM songs_in_lists
				WHERE song_id = $1 AND list_id = $2
			);
		"""

		values = (song_id, playlist_id)

		result: bool = await self.conn.fetchval(query, *values)

		return result

	async def create_playlist(
		self,
		title: str,
		owner_id: str
	):
		"""
		Creates a new playlist.

		:param title:
			The name of the playlist
		:type title: str

		:param owner_id:
			The discord ID of the user using the command, who owns this playlist.
		:type owner_id: str

		:raises DbInsertError:
			Raised when an error creating a playlist occurs.
		"""

		query = """
			INSERT INTO playlists(list_id, title, owner_id)
			VALUES (nextval('playlists_list_id_seq', $1, $2));
		"""

		values = (title, owner_id)

		try:
			await self.conn.execute(query, *values)
		except Exception as error:
			self.logger.debug(error)
			raise DbInsertError("Could not create a playlist.", values)

	async def get_playlists(
		self,
		owner_id: str
	) -> Union[List[str], None]:
		"""
		Get all playlists owned by a specific user.

		:param owner_id:
			The discord ID of the user to search for.
		:type owner_id: str

		:return:
			A list of the title of each playlist the user owns if any, None otherwise.
		:rtype: Union[List[str], None]
		"""

		query = """
			SELECT title FROM playlists
			WHERE owner_id = ($1);
		"""

		results = await self.conn.fetch(query, owner_id)

		if len(results) == 0:
			return None

		titles: List[str] = list()
		for result in results:
			titles.append(result.get('title'))

		return titles

	async def add_song_to_playlist(
		self,
		song: Song,
		playlist_title: str,
		user_id: str
	) -> str:
		"""
		Add a song to a playlist if it's owned by the calling user.

		:param song:
			The song to add.
		:type song: Song

		:param playlist_title:
			The title of the playlist to add the song to.
		:type playlist_title: str

		:param user_id:
			The discord ID of the calling user.
		:type user_id: str

		:return:
			A message to send to the calling user.
		:rtype: str
		"""

		if not await self.playlist_exists(playlist_title, user_id):
			try:
				self.create_playlist(playlist_title, user_id)
			except DbInsertError as error:
				message, *rest = error.args
				self.logger.error(message)
				self.logger.debug(rest)
				return "An error occured while creating the playlist."

		if not await self.song_exists(song):
			try:
				self.insert_song(song)
			except DbInsertError as error:
				message, *rest = error.args
				self.logger.error(message)
				self.logger.debug(rest)
				return "An error occured while adding the song."

		if not await self.song_matches_playlist(song, playlist_title, user_id):
			try:
				self.match_song_to_playlist(song, playlist_title, user_id)
			except DbInsertError as error:
				message, *rest = error.args
				self.logger.error(message)
				self.logger.debug(rest)
				return "An error occured while adding the song."

		return f"Added {song.title} to {playlist_title}."

	async def get_playlist_id(
		self,
		playlist_title: str,
		owner_id: str
	) -> Union[int, None]:
		"""
		Get the database ID of a playlist.

		:param playlist_title:
			The title of the playlist to search for.
		:type playlist_title: str

		:param owner_id:
			The ID of the owner of the playlist.
		:type owner_id: str

		:return:
			The ID of the playlist if it exists, None otherwise.
		:rtype: Union[int, None]
		"""

		query = """
			SELECT list_id
			FROM playlists
			WHERE title = $1 AND owner_id = $2;
		"""

		values = (playlist_title, owner_id)

		playlist_id: Union[int, None] = await self.conn.fetchval(query, *values)

		return playlist_id

	async def playlist_exists(
		self,
		playlist_title: str,
		owner_id: str
	) -> bool:
		"""
		Check if a playlist exists in the database.

		:param playlist_title:
			The title of the playlist to search for.
		:type playlist_title: str

		:param owner_id:
			The discord ID of the calling user.
		:type owner_id: str

		:return:
			True if a playlist with that title and owner exists.
		:rtype: bool
		"""

		query = """
			SELECT exists(SELECT * FROM playlists WHERE title = $1 AND owner_id = $2);
		"""

		values = (playlist_title, owner_id)

		result: bool = await self.conn.fetchval(query, *values)

		return result


class DbInsertError(Exception):
	"""
	Raised when an error related to INSERT occurs.
	"""
	pass
