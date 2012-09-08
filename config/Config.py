import json
import logging

class Config:
    # Name of configuration
    name = ""
    
    # Configuration data
    data = None
    
    # Global configuration data
    glob = None
    
    # Configuration path
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
        # Write the config file
        f = open(Config.configPath + self.name + ".config.json", "w")
        f.write(json.dumps(self.data))
        f.close()
        
    # Creates a user config with some default settings
    @staticmethod
    def createUserConfig(username, data):
        # Write the config file
        f = open(Config.configPath + username + ".config.json", "w")
        f.write(json.dumps(data, sort_keys = True, indent = 4))
        f.close()
        
    # Loads global config
    @staticmethod
    def loadGlobal():
        # Load the configuration file
        try:
            Config.glob = json.loads( open(Config.configPath + "global.config.json").read() )
        except Exception:
            # Probably doesn't exist, so create it with default settings
            data = {'HTTPHeaderVer': 'Firefox', 'debug': 'False'}
            
            # Write the config file
            f = open(Config.configPath + "global.config.json", "w")
            f.write(json.dumps(data, sort_keys = True, indent = 4))
            f.close()
        
    # Returns global config
    @staticmethod
    def getGlobal():
        return Config.glob
        
    @staticmethod    
    def saveGlobal():
        # Write the config file
        f = open(Config.configPath + "global.config.json", "w")
        f.write(json.dumps(Config.glob))
        f.close()
            
	# The rest of these methods simply allow this class to be treated as a dictionary 
    
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
