# queue.py
#
# Implementation of a queue to be used by music.py.


# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


from cogs.song import Song
from typing import List, Tuple, Union


class SongQueue():
	"""
	Class to manage queues of Song(s).
	Uses a list of Songs and adds some methods to simplify operations in the cogs.
	"""

	def __init__(self):
		self.songs = []

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
			if 1 <= index <= len(self.songs):
				return self.songs.pop(index - 1)

		return None

	def get_songs(self) -> List[Song]:
		"""
		Simple getter.

		:return:
			The actual list of Songs.
		:rtype: List[Song]
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

	def insert(self, song: Song, index: int) -> str:
		"""
		Inserts a song at position index.

		:param song:
			The song to insert.
		:type song: Song

		:param index:
			The index of the position to insert the song into.
		:type index: int

		:raises IndexError:
			If index is out of range.

		:return:
			A message about the result of the operation.
		:rtype: str
		"""

		if self.is_empty():
			self.push(song)
			return "The queue was empty, added in first place."

		# we use size+1 because Music.move removes a song first
		elif 1 <= index <= len(self.songs) + 1:
			# insert song at index using slice indexing
			self.songs[index - 1:index - 1] = [song]
			return f"Moved \"{song.title}\" to position {index}."

		else:
			raise IndexError("(queue.insert)", f"size: {len(self.songs)}", f"index: {index}")

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
		"""

		size = self.get_size()

		if self.is_empty():
			return "The queue is empty!"

		elif index1 < 1 or index1 > size:
			# Index check to get the correct message.
			return f"There's no song with that index! The current size of the queue is {size}."

		elif index2 < 1 or index2 > size:
			# Index check for the message + avoid popping a song and not inserting it.
			return f"That's out of bounds! The current size of the queue is {size}."

		else:
			song = self.pop(index1)  # Pass index1 as is, see pop().
			res = self.insert(song, index2)  # Pass index2 as is, see insert().
			return res

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
