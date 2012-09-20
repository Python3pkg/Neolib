""":mod:`Config` -- Contains the Config class

.. module:: Config
   :synopsis: Contains the Config class
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

import json
import logging

class Config:
    
    """Provides an interface for accessing and storing configuration information to a local file
    
    This class contains an interface for communicating data in a JSON format to and from a local
    configuration file. It contains functionality for accessing a global configuration as well
    as local user configuration files. Each instance of Config represents one configuration file
    which is described in its 'name' attribute. 
    
    Attributes
       name (str) - Config's name
       data (dictionary) - All configuration data
       glob (dictionary) - All global configuration data
       configPath (str) - The default config path to save configuration files to
       
    Initialization
       Config(name)
       
       Loads a configuration file using name
       
       Attempts to load a configuration file by using the given name. The file
       is loaded by appending the configuration path to name and finally
       '.config.json'. Does nothing if the file does not exist, otherwise
       it loads and interprets the JSON content into itself.
       
       Parameters
          name (str) - Config's name
        
    Example
       >>> Config.configPath = '/config/'
       >>> cf = Config('test') # Loads '/config/test.config.json'
       >>> cf['doSomething'] = 'False'
       >>> cf.saveConfig()
    """
    
    name = ""
    data = None
    glob = None
    configPath = None
    
    def __init__(self, name):
		# Load the configuration file
        try:
            self.data = json.loads( open(Config.configPath + name + ".config.json").read() )
            self.name = name
        except IOError:
            pass
        except Exception:
            logging.getLogger("neolib.config").exception("Failed to load configuration file: " + path + name + ". May be corrupted.")
            data = None
		
    def saveConfig(self):
        """ Saves the current configuration data to it's associated file
        """
        # Write the config file
        f = open(Config.configPath + self.name + ".config.json", "w")
        f.write(json.dumps(self.data))
        f.close()
        
    # Creates a user config with some default settings
    @staticmethod
    def createUserConfig(username, data):
        """ Creates a configuration file using username and data, returns Config object
        
        Uses the given username as the name of the configuration and
        the information stored in data to create a new configuration.
        Returns the Config object representing the new configuration.
        
        Parameters
           username (str) - Username to use in creating the config
           data (dictionary) - Data to store in the configuration
           
        Returns
           Config - The new configuration
        """
        # Write the config file
        f = open(Config.configPath + username + ".config.json", "w")
        f.write(json.dumps(data, sort_keys = True, indent = 4))
        f.close()
        
        return Config(username)
        
    # Loads global config
    @staticmethod
    def loadGlobal():
        """ Loads global configuration file into Config.glob
        
        Searches for and loads 'global.config.json' using the stored
        configuration path and stores its contents in Config.glob. Since
        Neolib uses the global configuration file, if the function fails
        to find a global configuration file it creates it and fills it with
        default configuration data. If a configuration file is created in this
        way, the function proceeds to load it into Config.glob. 
        """
        # Load the configuration file
        try:
            Config.glob = json.loads( open(Config.configPath + "global.config.json").read() )
        except Exception:
            # Probably doesn't exist, so create it with default settings
            data = {"HTTPHEADER": {"HTTPVER": "1.1",
                   "USER-AGENT": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1",
                   "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "ACCEPT-LANGUAGE": "en-us,en;q=0.5",
                   "ACCEPT-ENCODING": "gzip, deflate",
                   "CONNECTION": "close"}}
            
            # Write the config file
            f = open(Config.configPath + "global.config.json", "w")
            f.write(json.dumps(data, sort_keys = True, indent = 4))
            f.close()
            
            Config.glob = json.loads( open(Config.configPath + "global.config.json").read() )
        
    # Returns global config
    @staticmethod
    def getGlobal():
        """Returns the global configuration
        """
        return Config.glob
        
    @staticmethod    
    def saveGlobal():
        """ Saves the global configuration contents to the global configuration file
        """
        # Write the config file
        f = open(Config.configPath + "global.config.json", "w")
        f.write(json.dumps(Config.glob))
        f.close()
    
    def __getitem__(self, key):
        return self.data[key]
        
    def __setitem__(self, key, value):
        self.data[key] = value
        
    def __delitem__(self, key):
        self.data.pop(key)
        
    def __contains__(self, key):
        if key in self.data:
            return True
        else:
            return False
            
    def __iter__(self):
        for item in self.data:
            yield self.data[item]
            
    def __len__(self):
        return len(self.data)
            
    def empty(self):
        return self.empty
