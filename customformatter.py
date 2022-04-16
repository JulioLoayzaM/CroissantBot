# CroissantBot/customformatter.py

"""
Defines a logging formatter to customize the logger's output:
	- sets the format: "time - logger - level - log (file:line)"
	- adds colour to the levels


The MIT License (MIT)

Copyright (c) 2021-present JulioLoayzaM

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import logging


class CustomFormatter(logging.Formatter):
	"""Custom logging formatter to colour-code the levels.
	"""

	# Colours for formatting console text
	BLUE      = '\033[94m'
	CYAN      = '\033[96m'
	YELLOW    = '\033[93m'
	RED       = '\033[91m'
	BOLDRED   = '\033[31;20m'
	ENDC      = '\033[0m'

	# The extra spaces are intended, just in case.
	format_prefix = "%(asctime)s - "
	format_level  = "%(levelname)s"
	format_body   = " - %(message)s (%(module)s:%(funcName)s:%(lineno)d)"

	FORMATS = {
		logging.DEBUG:    format_prefix + BLUE + format_level + ENDC + format_body,
		logging.INFO:     format_prefix + CYAN + format_level + ENDC + format_body,
		logging.WARNING:  format_prefix + YELLOW + format_level + ENDC + format_body,
		logging.ERROR:    format_prefix + RED + format_level + ENDC + format_body,
		logging.CRITICAL: format_prefix + BOLDRED + format_level + ENDC + format_body,
	}

	def format(self, record: logging.LogRecord):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)
