# CroissantBot/cogs/ext/db.py

"""
For all database connection needs.

This module provides :py:class:`DatabaseConnection`:
	The base connection class with three methods: :py:func:`DatabaseConnection.connect`,
	:py:func:`DatabaseConnection.close` and :py:func:`DatabaseConnection.is_connected`.
"""

# The MIT License (MIT)

# Copyright (c) 2021-present JulioLoayzaM

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

import asyncio
import asyncpg
import logging


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

		try:
			conn = await asyncpg.connect(
				host=host, port=port, user=user, password=password, database=database, loop=loop
			)
		except Exception as error:
			raise Exception("Couldn't connect to the database.", error)

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
