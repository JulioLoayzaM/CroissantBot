# test_queue.py

import pytest
import random

from cogs.ext.queue import SongQueue
from cogs.ext.song import Song
from typing import List


NUMBER_OF_SONGS = 10
N1 = NUMBER_OF_SONGS // 3
N2 = 2 * NUMBER_OF_SONGS // 3


def song_factory(n: int) -> List[Song]:
	"""
	Generates n songs.
	"""
	if n < 1:
		raise IndexError("Can't generate less than 1 song.")
	songs: List[Song] = list()
	for i in range(n):
		songs.append(
			Song(
				f"song_{i+1}",
				f"file_{i+1}",
				f"url_{i+1}",
				f"thumbnail_{i+1}"
			)
		)
	return songs


@pytest.fixture
def example_songs() -> List[Song]:
	songs = song_factory(NUMBER_OF_SONGS)
	return songs


@pytest.fixture
def example_queue(example_songs) -> SongQueue:
	queue = SongQueue()
	songs = example_songs
	for song in songs:
		queue.push(song)
	return queue


def test_random_pop(example_queue):
	queue = example_queue
	i = random.randint(1, queue.get_size())
	song = queue.pop(i)
	assert (song.title == f"song_{i}")


@pytest.mark.parametrize("n", [N1, N2])
def test_random_pop_mult(example_queue, n: int):
	queue = example_queue
	size = queue.get_size()
	old_n = n
	while (size > 0) and (n > 0):
		i = random.randint(1, size)
		queue.pop(i)
		size -= 1
		n -= 1
	assert (queue.get_size() == NUMBER_OF_SONGS - old_n)


def test_clear(example_queue):
	queue: SongQueue = example_queue
	queue.clear()
	assert queue.is_empty()


@pytest.mark.parametrize("n", [N1, N2])
def test_skip(example_queue, n):
	queue: SongQueue = example_queue
	queue.skip(n)
	song = queue.pop()
	assert (song.title == f"song_{n+1}")


def test_remove(example_queue):
	queue: SongQueue = example_queue
	size = queue.get_size()
	b, _ = queue.remove(0)
	assert not b
	b, _ = queue.remove(size + 1)
	assert not b
	i = random.randint(1, size)
	b, title = queue.remove(i)
	assert b
	assert title == f"song_{i}"


def test_insert(example_songs):
	songs = example_songs
	queue = SongQueue()
	half = len(songs) // 2
	# Insert when queue is empty.
	r = queue.insert(songs[0], 2)
	assert r == 0
	# Insert first.
	r = queue.insert(songs[1], 1)
	assert r == 1
	# Insert many.
	for i in range(half):
		r = queue.insert(songs[i], 2)
		assert r == 2
	assert queue.get_size() == (half + 2)
	# Insert after queue size.
	size = queue.get_size()
	r = queue.insert(songs[-1], 2 * size)
	assert r == (size + 1)
