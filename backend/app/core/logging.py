import logging
import sys


def setup_logging():
	"""
	Configures logging for the application.
	"""
	# Get the root logger
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)  # Set the minimum level of messages to handle

	# Create a handler to write log messages to the console (stdout)
	handler = logging.StreamHandler(sys.stdout)

	# Create a formatter and set it for the handler
	# This format is a good starting point for structured logging
	formatter = logging.Formatter(
		'{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
	)
	handler.setFormatter(formatter)

	# Add the handler to the logger
	# Avoid adding handlers if they already exist
	if not logger.handlers:
		logger.addHandler(handler)


# You can also get a specific logger for your app
log = logging.getLogger(__name__)
