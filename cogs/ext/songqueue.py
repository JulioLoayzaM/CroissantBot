# CroissantBot/cogs/ext/queue.py

"""
Implementation of a queue to be used by the :py:mod:`music` cog.
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

from collections import deque
from cogs.ext.song import Song
from typing import Tuple, Union, Deque


class SongQueue():
	"""
	Class to manage queues of Song(s).
	Uses a list of Songs and adds some methods to simplify operations in the cogs.
	"""

	def __init__(self):
		self.songs = deque()

	def push(self, song: Song):
		"""
		Add a song at the end of the queue.

		:param song:
			The song to append.
		:type song: Song
		"""
		self.songs.append(song)

	def pop(self, index: int = 1) -> Union[Song, None]:
		"""
		Pop the song at position index, if it exists.

		:param index:
			The index of the song to pop. 1 by default to pop the first song.
		:type index: int

		:return:
			The song at position index if it exists, None if not.
		:rtype: Union[Song, None]
		"""

		if len(self.songs) > 0:
			if index == 1:
				return self.songs.popleft()
			elif 1 < index <= len(self.songs):
				song: Song = self.songs[index - 1]
				del self.songs[index - 1]
				return song
		return None

	def get_songs(self) -> Deque[Song]:
		"""
		Simple getter.

		:return:
			The actual deque of Songs.
		:rtype: deque[Song]
		"""
		return self.songs

	def get_size(self) -> int:
		"""
		Simple getter.

		:return:
			The length of the list of songs.
		:rtype: int
		"""
		return len(self.songs)

	def is_empty(self) -> bool:
		"""
		Check the length of the list to determine whether the queue is empty.

		:return:
			True if the list is empty, False otherwise.
		:rtype: bool
		"""
		return len(self.songs) == 0

	def clear(self):
		"""
		Remove all songs from the queue.
		"""
		self.songs.clear()

	def skip(self, index: int):
		"""
		Pops 'index' songs to skip them.

		:param index:
			The number of songs to skip.
		:type index: int

		:raises IndexError:
			If the index is out of bounds.
		"""
		if (index > 0) and self.is_empty():
			raise EmptyQueueError

		if (index > len(self.songs)) or (index < 0):
			raise IndexError

		while index > 0:
			self.pop()
			index -= 1

	def remove(self, index: int) -> Tuple[bool, str]:
		"""
		Removes the song at position index.

		:param index:
			The index of the song to remove.
		:type index: int

		:return:
			The result of the operation.
		:rtype: bool

		:return:
			A message to pass to the user: a reason if an error occured,
			or the title of the song if not.
		:rtype: str
		"""
		size = self.get_size()

		if self.is_empty():
			return False, "The queue is empty."

		elif index < 1:
			return False, "Index can't be lower than 1."

		elif index > size:
			return False, f"There's no song with that index! The queue has {size} songs."

		else:
			song = self.pop(index)
			# Since the index is pre-checked, there sould be no need to check
			# if song is None.
			return True, f"{song.title}"

	def insert(self, song: Song, index: int) -> int:
		"""
		Inserts a song at position index.

		:param song:
			The song to insert.
		:type song: Song

		:param index:
			The index of the position to insert the song into.
		:type index: int

		:return:
			If the queue is empty, returns 0. Else, it returns the index.
		:rtype: int

		.. note::
			If index is less than 1, inserts the song at the beginning.
			If the index is greater than the size of the queue, the song is simply \
			appended to the end of the queue.
		"""

		if self.is_empty():
			self.push(song)
			return 0

		else:
			if index <= 1:
				self.songs.appendleft(song)
				return 1
			elif 1 < index <= len(self.songs):
				self.songs.insert(index - 1, song)
				return index
			else:
				self.songs.append(song)
				return len(self.songs)

	def move(self, index1: int, index2: int) -> str:
		"""
		Moves the song from position index1 to position index2 in the queue.

		:param index1:
			The position of the song to be moved.
		:type index1: int

		:param index2:
			Where to move the song to.
		:type index2: int

		:raises IndexError:
			If any index is out of range.

		:return:
			A message about the result of the operation
		:rtype: str

		.. warning::
			This method only checks if the first index is valid, i.e. corresponds to \
			a song in the queue.
			If the second index is less than 1, the song is left-appended.
			If it's greater than the queue size, the song is appended.
		"""

		size = self.get_size()

		if self.is_empty():
			return "The queue is empty!"

		elif index1 < 1 or index1 > size:  # Index check to get the correct message.
			return f"There's no song with that index! The current size of the queue is {size}."

		else:
			song = self.pop(index1)  # Pass index1 as is, see pop().
			res = self.insert(song, index2)  # Pass index2 as is, see insert().
			if res == 0:
				return "The queue was empty, added in first place."
			else:
				return f"Moved \"{song.title}\" to position {res}."

	def get_song_info(self, index: int):
		"""
		Unused.
		"""
		if (index > len(self.songs) - 1) or (index < 0):
			raise IndexError
		else:
			song = self.songs[index]
			return song


class EmptyQueueError(Exception):
	"""
	Raised when attempting an operation on an empty queue
	"""
	pass
