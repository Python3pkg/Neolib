""":mod:`Configuration` -- User-based and global configuration handling

.. module:: Configuration
   :synopsis: User-based and global configuration handling
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from collections import MutableMapping
from neolib.http.Page import Page
import logging
import json

class Configuration(MutableMapping):
    
    """Provides an interface for global and user-based configuration handling
    
    Subclasses the MutableMapping ABC to provide a standard dictionary interface
    for accessing and storing configuration information. Utilizes the __dict__
    property to store all configuration data as if they were defined class
    attributes. Provides static initialization and retrieval functions for
    initializing a global configuration from a defined file and allowing
    individual sections of a program access to the global configuration. Writes
    and reads all configuration data in the JSON format.
    
    Attributes
       path (str) -- Path to the configuration file (defaults to 'config.json')
       
    Initialization
       Configuration(data)
       
       Initializes the configuration class with configuration data.
       
       Note Configuration.getConfig() should be used rather than directly
       initializing an instance of this class.
       
       Parameters
          data (dict) -- Dictionary of data to load the class with
        
    Example
       >>> if Configuration.initialize():
       ...     c = Configuration.getConfig()
       ...     c.core.addSection("uab")
       ...     c.core.uab.waitTime = 5
       ...     c.write()
    """
    
    path = "config.json"
    _config = None
    
    def __init__(self, data):
        self.__dict__ = data

    def write(self):
        """ Writes current configuration to Configuration.path, returns status
           
        Returns
           bool - True if successful, False otherwise
        """
        Configuration._writeConfig()

    def addSection(self, name):
        """ Adds an empty child section to the current configuration class
        
        Parameters
           name (str) -- Name of the child section
        """
        self.__dict__[name] = Configuration({})
        
    def toDict(self):
        """ Returns a dictionary whose contents reflect the contents of the configuration class
           
        Returns
           dict - Dictionary of class content
        """
        return self.__dict__
    
    def __getitem__(self, key):
        return self.__dict__[key]
        
    def __setitem__(self, key, value):
        # Ensures dictionaries are converted to Configuration objects
        if isinstance(value, dict):
            value = Configuration(value)
        self.__dict__[key] = value
        
    def __delitem__(self, key):
        del self.__dict__[key]
        
    def __iter__(self):
        for item in self.__dict__:
            yield item
            
    def __len__(self):
        return len(self.__dict__)
    
    @staticmethod
    def initialize():
        """ Attempts to load default configuration from Configuration.path, returns status
        
        Loads the contents of the file referenced in Configuration.path and
        parses it's JSON contents. Iterates over the contents of the resulting
        dictionary and converts the contents into a tiered instance of 
        Configuration classes. If no file is found in Configuration.path,
        automatically generates and sets a default configuration. The loaded
        configuration content can be accessed via Configuration.getConfig().
           
        Returns
           bool - True if successful, False otherwise
        """
        try:
            f = open(Configuration.path, 'r')
            data = f.read()
            f.close()
        except Exception:
            Configuration._createDefault() # Assumes the file does not exist or is not readable
            return True
            
        try:
            Configuration._config = Configuration(json.loads(data))
            Configuration._makeConfig(Configuration._config)
        except Exception as e:
            logging.getLogger("neolib.config").exception("Failed to read configuration file: " + Configuration.path)
            return False
            
        return True
        
    @staticmethod
    def getConfig():
        """ Returns the contents loaded from Configuration.initialize()
           
        Returns
           Configuration - Tiered configuration object containing contents loaded from Configuration.initialize()
        """
        return Configuration._config
    
    @staticmethod
    def loaded():
        """ Returns whether the configuration file has been loaded or not
           
        Returns
           bool - Whether Configuration.initialize() has been called yet or not
        """
        return bool(Configuration._config)
        
    @staticmethod
    def _writeConfig():
        try:
            f = open(Configuration.path, 'w')
            c = Configuration._makeDict(Configuration._config)
            f.write(json.dumps(c, sort_keys = True, indent = 4)) # Produces JSONified version of configuration data
            f.close()
            
            Configuration._makeConfig(Configuration._config)
        except Exception:
            logging.getLogger("neolib.config").exception("Failed to write configuration file: " + Configuration.path)
            return False
            
        return True

    @staticmethod
    def _makeDict(c):
        # Uses recursion to rebuild the tiered config object from the bottom up as a dictionary
        for item in c:
            if isinstance(c[item], MutableMapping):
                Configuration._makeDict(c[item])
                c.__dict__[item] = dict(c[item])
        
        return dict(c)

    @staticmethod
    def _makeConfig(c):
        if not isinstance(c, dict) and not isinstance(c, MutableMapping): return # We don't need to handle other data
        if len(c) <= 0 and not isinstance(c, MutableMapping):
            c = Configuration(c)
            return
            
        for key in c:
            if isinstance(c[key], dict):
                c[key] = Configuration(c[key])
                Configuration._makeConfig(c[key])

    @staticmethod
    def _createDefault():
        default = {'core': {'HTTPHeaders': Page._defaultVars, 'Debug': 'False'}, 'users': {}} # Default data
        
        try:
            f = open(Configuration.path, 'w')
            f.write(json.dumps(default, sort_keys = True, indent = 4))
            f.close()
        except Exception:
            logging.getLogger("neolib.config").exception("Failed to create configuration file: " + path)
            return False
            
        Configuration._config = Configuration(default)
        Configuration._makeConfig(Configuration._config)
                
