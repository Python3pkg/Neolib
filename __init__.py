import logging
from datetime import datetime
from neolib.HTMLFilter import HTMLFilter

# Intention of this file is to setup logging whenever the library is initialized.

# Sets up to log to a file that looks as such: Neolib 2012-08-18 23-49-16.log.txt
logFileName = datetime.today().strftime("Neolib %Y-%m-%d %H-%M-%S") + ".log.txt"

# Creates a logger instance for the library
logger = logging.getLogger("neolib")
logger.setLevel(logging.DEBUG)

# Creates the file handler and set's delay to True so it only creates the file when a request is issued
fh = logging.FileHandler(logFileName, delay = True)
fh.setLevel(logging.DEBUG)

# Creates the console handler 
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Sets a format for all log entries to follow. Refer to Python documents for LogRecord attributes to see what each of these variables represent
format = logging.Formatter("[%(asctime)s] %(name)s (%(levelname)s) in %(filename)s : %(lineno)d - %(message)s") 

# Set the format for both the console and file handle
fh.setFormatter(format) 
ch.setFormatter(format)

# Set a filter to ensure the file and console handler don't log HTML content
fh.addFilter(HTMLFilter())
ch.addFilter(HTMLFilter())

# Add the console and file handler
logger.addHandler(fh)
logger.addHandler(ch)
