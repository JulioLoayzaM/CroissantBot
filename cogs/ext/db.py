# db.py

"""
For all database connection needs.

This module provides:

	:py:class:`DatabaseConnection`:
		The base class with three methods: :py:func:`DatabaseConnection.connect`,
		:py:func:`DatabaseConnection.close` and :py:func:`DatabaseConnection.is_connected`.

	:py:class:`MusicDatabaseConnection`:
		A class to provide an interface for managing the playlists
		stored in the database.
"""

# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.

import asyncio
import asyncpg
import logging

from cogs.ext.song import Song
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
	The base class to represent a connection to a PostgreSQL database.

	:param logger_name:
		The name of the logger to be used by the connection.
	:type logger_name: str
	"""

	def __init__(self, logger_name: str):
		"""
		Initializes an instance with no connection and a logger.

		:param logger_name:
			The name of the logger to be used by the connection.
		:type logger_name: str
		"""
		self.conn: asyncpg.Connection = None
		self.logger = logging.getLogger(logger_name)
		self.db_name = ""

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
		Connect to a database using the credentials provided. Stores connection in `self.conn`.

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

		self.db_name = database

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
			self.logger.debug(f"{WARNING}Closed:{ENDC} connection to the database {self.db_name}.")
			return True

		else:
			self.logger.warning(f"No connection to database '{self.db_name}' to close.")
			return False

	async def is_connected(
		self
	) -> bool:
		"""
		Check if the connection is active.

		:return:
			True if there's a connection, False otherwise.
		:rtype: bool
		"""

		if self.conn is None:
			return False
		else:
			return not self.conn.is_closed()


class MusicDatabaseConnection(DatabaseConnection):
	"""
	A class to provide an interface to manage the playlists used by the
	`playlist` group of commands.

	:param logger_name:
		The name of the logger to be used by this connection.
	:type logger_name: str
	"""

	def __init__(self, logger_name: str):
		"""
		Initializes a new instance.

		:param logger_name:
			The name of the logger to be used by this connection.
		:type logger_name: str
		"""
		super().__init__(logger_name)

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
			raise DbInsertError("Could not insert a song.", str(song))

	async def get_song_id(
		self,
		song_url: str
	) -> Union[int, None]:
		"""
		Get the database ID of a song.

		:param song_url:
			The URL of the song to search for.
		:type song_url: str

		:return:
			The ID of the song if it exists, None otherwise.
		:rtype: Union[int, None]
		"""

		query = """
			SELECT song_id
			FROM songs
			WHERE url = $1;
		"""

		song_id: Union[int, None] = await self.conn.fetchval(query, song_url)

		return song_id

	async def get_song_url(
		self,
		song_id: int
	) -> Union[str, None]:
		"""
		Get the URL of a song.

		:param song_id:
			The song ID to get the URL from.
		:type song_id: int

		:return:
			The URL of the song if it exists, None otherwise.
		:rtype: Union[str, None]
		"""

		query = """
			SELECT url
			FROM songs
			WHERE song_id = $1;
		"""

		url: Union[str, None] = await self.conn.fetchval(query, song_id)

		return url

	async def get_titles(
		self,
		song_ids: List[int]
	) -> List[str]:
		"""
		Get the titles of a list of songs.

		:param song_ids:
			A list of song IDs to get. It SHOULD NOT be empty, and the IDs SHOULD be in songs.
		:type song_ids: List[int]

		:return:
			A list of the corresponding song titles. Since the IDs SHOULD be in the database,
			no value should be empty. However, no check is done at this point.
		:rtype: List[str]
		"""

		query = """
			SELECT title
			FROM songs
			WHERE song_id = $1;
		"""

		titles: List[str] = list()
		for sid in song_ids:
			titles.append(await self.conn.fetchval(query, sid))

		return titles

	async def get_urls(
		self,
		song_ids: List[int]
	) -> List[str]:
		"""
		Get the URLs of a list of songs.

		:param song_ids:
			A list of song IDs to get. It SHOULD NOT be empty, and the IDs SHOULD be in songs.
		:type song_ids: List[int]

		:return:
			A list of the corresponding song URLs. Since the IDs SHOULD be in the database,
			no value should be empty. However, no check is done at this point.
		:rtype: List[str]
		"""

		query = """
			SELECT url
			FROM songs
			WHERE song_id = $1
			ORDER BY song_id;
		"""

		urls: List[str] = list()
		for sid in song_ids:
			urls.append(await self.conn.fetchval(query, sid))

		return urls

	async def get_titles_in_playlist(
		self,
		playlist_title: str,
		owner_id: str
	) -> Union[List[str], None]:
		"""
		Get the title of all songs in a specific playlist.

		:param playlist_title:
			The title of the playlist to get the songs from.
		:type playlist_title: str

		:param owner_id:
			The discord ID of the owner of the playlist.
		:type owner_id: str

		:return:
			A list of the titles of all the songs in the playlist, or None if the playlist
			doesn't exist, or if it doesn't have any songs.
		:rtype: Union[List[str], None]
		"""

		playlist_id = await self.get_playlist_id(playlist_title, owner_id)
		if playlist_id is None:
			return None

		query = """
			SELECT song_id
			FROM songs_in_lists
			WHERE list_id = $1
			ORDER BY song_id;
		"""

		results = await self.conn.fetch(query, playlist_id)

		if len(results) == 0:
			return None

		ids: List[int] = list()
		for result in results:
			ids.append(result.get('song_id'))

		songs = await self.get_titles(ids)
		if len(songs) == 0:
			return None
		else:
			return songs

	async def get_song_from(
		self,
		index: int,
		playlist_title: str,
		owner_id: str
	) -> Union[str, None]:
		"""
		Get a song from a playlist by its index.

		:param index:
			The index of the song in the playlist (as displayed with
			:func:`get_titles_in_playlist`).
		:type index: int

		:param playlist_title:
			The title of the playlist to get the song from.
		:type playlist_title: str

		:param owner_id:
			The discord ID of the owner of the playlist.
		:type owner_id: str

		:return:
			The song's URL if it exists in the playlist, None otherwise.
		:rtype: Union[str, None]
		"""

		playlist_id = await self.get_playlist_id(playlist_title, owner_id)
		if playlist_id is None:
			return None

		# Get the song ID.
		query = """
			SELECT song_id
			FROM songs_in_lists
			WHERE list_id = $1
			ORDER BY song_id
			LIMIT 1
			OFFSET $2;
		"""
		values = (playlist_id, index - 1)
		song_id = await self.conn.fetchval(query, *values)

		if song_id is None:
			return None
		song = await self.get_song_url(song_id)

		return song

	async def get_songs_in_playlist(
		self,
		playlist_title: str,
		owner_id: str
	) -> Union[List[str], None]:
		"""
		Get the URLs of all songs in a specific playlist.

		:param playlist_title:
			The title of the playlist to get the songs from.
		:type playlist_title: str

		:param owner_id:
			The discord ID of the owner of the playlist.
		:type owner_id: str

		:return:
			A list of the URLs of all the songs in the playlist, or None if the playlist
			doesn't exist, or if it doesn't have any songs.
		:rtype: Union[List[str], None]
		"""

		playlist_id = await self.get_playlist_id(playlist_title, owner_id)
		if playlist_id is None:
			return None

		query = """
			SELECT song_id
			FROM songs_in_lists
			WHERE list_id = $1;
		"""

		results = await self.conn.fetch(query, playlist_id)

		if len(results) == 0:
			return None

		ids: List[int] = list()
		for result in results:
			ids.append(result.get('song_id'))

		songs = await self.get_urls(ids)
		if len(songs) == 0:
			return None
		else:
			return songs

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

		song_id: Union[int, None] = await self.get_song_id(song.url)

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

		song_id = await self.get_song_id(song.url)
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

	async def match_song_to_playlist(
		self,
		song: Song,
		playlist_title: str,
		owner_id: str
	):
		"""
		Match a song to a playlist, ie. create a row in songs_in_lists.

		:param song:
			The song to match. It must already be in the database.
		:type song: Song

		:param playlist_title:
			The title of the playlist to match. It must already be in the database.
		:type playlist: str

		:param owner_id:
			The owner of the playlist to match. It must already be in the database.
		:type owner_id: str
		"""

		song_id = await self.get_song_id(song.url)
		if song_id is None:
			raise DbInsertError(
				"Can't match a song that's not in the database.",
				str(song)
			)

		playlist_id = await self.get_playlist_id(playlist_title, owner_id)
		if playlist_id is None:
			raise DbInsertError(
				"Can't match a playlist that's not in the database.",
				playlist_title,
				owner_id
			)

		query = """
			INSERT INTO songs_in_lists(song_id, list_id)
			VALUES ($1, $2);
		"""

		values = (song_id, playlist_id)

		try:
			await self.conn.execute(query, *values)
		except Exception as error:
			self.logger.debug(error)
			raise DbInsertError(
				"Could not match song with playlist.",
				f"song_id: {song_id}",
				f"playlist_id: {playlist_id}",
				str(song),
				f"title: {playlist_title}",
				f"owner_id: {owner_id}"
			)

	async def remove_song_from(
		self,
		title: str,
		owner_id: str,
		index: int
	):
		"""
		Removes a song from a playlist.

		:param title:
			The title of the playlist.
		:type title: str

		:param owner_id:
			The owner of the playlist.
		:type owner_id: str

		:param index:
			The index of the song in the playlist.
		:type index: int

		:raises NotFoundError:
			Raised when the song is not in the database.

		:raises DbInsertError:
			Raised when an error removing the song occurs.
		"""

		song_url = await self.get_song_from(index, title, owner_id)
		if song_url is None:
			raise NotFoundError(
				"Can't remove a song that's not in the database.",
				song_url
			)

		query = """
			DELETE FROM songs_in_lists
			USING songs
			WHERE songs_in_lists.song_id = songs.song_id AND songs.url = $1;
		"""

		try:
			await self.conn.execute(query, song_url)
		except Exception as error:
			self.logger.debug(error)
			raise DbInsertError(
				"Could not remove song from playlist.",
				f"song_url: {song_url}",
				f"title: {title}",
				f"owner_id: {owner_id}"
			)

	async def create_playlist(
		self,
		title: str,
		owner_id: str
	):
		"""
		Create a new playlist if one with that title and owner doesn't already exist.

		:param title:
			The name of the playlist.
		:type title: str

		:param owner_id:
			The discord ID of the user using the command, who owns this playlist.
		:type owner_id: str

		:raises DbInsertError:
			Raised when an error occurs while creating the list or when the playlist
			already exists.
		"""

		exists = await self.playlist_exists(title, owner_id)

		values = (title, owner_id)

		if exists:
			raise DbInsertError("A playlist with that name already exists!", values)

		query = """
			INSERT INTO playlists(list_id, title, owner_id)
			VALUES (nextval('playlists_list_id_seq'), $1, $2);
		"""

		try:
			await self.conn.execute(query, *values)

		except Exception as error:
			self.logger.debug(error)
			raise DbInsertError("Could not create the playlist.", values)

	async def delete_playlist(
		self,
		title: str,
		owner_id: str
	):
		"""
		Delete a playlist if it exists.

		:param title:
			The name of the playlist.
		:type title: str

		:param owner_id:
			The discord ID of the user using the command, who owns this playlist.
		:type owner_id: str

		:raises DbInsertError:
			Raised when an error occurs while deleting the list.
		"""

		plid = await self.get_playlist_id(title, owner_id)

		values = (title, owner_id)

		if plid is None:
			raise DbInsertError("No playlist with that name exists!", values)

		query = """
			DELETE FROM playlists
			WHERE list_id = $1;
		"""

		try:
			await self.conn.execute(query, plid)

		except Exception as error:
			self.logger.debug(error)
			raise DbInsertError("Could not delete the playlist.", values)

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
		Creates the playlist if it doesn't exist.

		:param song:
			The song to add.
		:type song: Song

		:param playlist_title:
			The title of the playlist to add the song to.
		:type playlist_title: str

		:param user_id:
			The discord ID of the calling user.
		:type user_id: str

		:raises DbInsertError:
			When a problem creating the playlist/inserting the song/adding it
			to the playlist occurs.

		:return:
			A message to send to the calling user.
		:rtype: str
		"""

		# Notify the user when a playlist is created.
		pre = ""
		if not await self.playlist_exists(playlist_title, user_id):
			try:
				await self.create_playlist(playlist_title, user_id)
				pre = f"Created playlist {playlist_title}.\n"
			except DbInsertError as error:
				message, *rest = error.args
				self.logger.error(message)
				self.logger.debug(rest)
				raise DbInsertError(message)

		if not await self.song_exists(song):
			try:
				await self.insert_song(song)
			except DbInsertError as error:
				message, *rest = error.args
				self.logger.error(message)
				self.logger.debug(rest)
				raise DbInsertError("An error occured while adding the song.")

		if not await self.song_matches_playlist(song, playlist_title, user_id):
			try:
				await self.match_song_to_playlist(song, playlist_title, user_id)
			except DbInsertError as error:
				message, *rest = error.args
				self.logger.error(message)
				self.logger.debug(rest)
				raise DbInsertError("An error occured while adding the song.")

		return f"{pre}{song.title} to {playlist_title}."

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


class NotFoundError(Exception):
	"""
	Raised when an error related to a missing result occurs.
	"""
	pass
