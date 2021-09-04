# customformatter.py

# Defines a logging formatter to customize the logger's output:
#	- sets the format: "time - logger - level - log (file:line)"
#	- adds colour to the levels

import logging

class CustomFormatter(logging.Formatter):
	"""
	Custom logging formatter to colour-code the levels.
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