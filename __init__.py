import logging
from datetime import datetime
from RegLib import RegLib

# Sets up to log to a file that looks as such: Neolib 2012-08-18 23-49-16.log.txt
logFileName = datetime.today().strftime("Neolib %Y-%m-%d %H-%M-%S") + ".log.txt"

# Creates a logger instance for the library
logger = logging.getLogger("neolib")
logger.setLevel(logging.DEBUG)

# Creates the file handler
fh = logging.FileHandler(logFileName)
fh.setLevel(logging.DEBUG)

# Creates the console handler 
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Sets a format for all log entries to follow. Refer to Python documents for LogRecord attributes to see what each of these variables represent
format = logging.Formatter("[%(asctime)s] %(name)s (%(levelname)s) in %(filename)s : %(lineno)d - %(message)s") 

# Set the format for both the console and file handle
fh.setFormatter(format)
ch.setFormatter(format)

# Add the console and file handler to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Load our regex library for use by various modules
RegLib.loadReg()