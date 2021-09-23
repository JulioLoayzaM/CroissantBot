# song.py
#
# Small class to represent a song for the queue.

# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.

class Song():

	def __init__(self, title: str, file: str, url: str, thumbnail: str):

		self.title = title
		self.file  = file
		self.url   = url
		self.thumbnail = thumbnail
