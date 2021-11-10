# song.py

"""
Small class to represent a song for the queue.
"""

# Copyright (C) 2021 JulioLoayzaM
#
# You may use, distribute and modify this code under
# the terms of the MIT license.
#
# See the LICENSE file for more details.


class Song():
	"""
	A class to represent a song. Stores the title, the name of the downloaded file,
	the URL and the thumbnail URL.
	"""

	def __init__(self, title: str, file: str, url: str, thumbnail: str):

		self.title = title
		self.file  = file
		self.url   = url
		self.thumbnail = thumbnail

	def __str__(self):
		return f"{self.title} - {self.url}"
