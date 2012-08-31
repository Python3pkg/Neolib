import json
import logging

class Config:
    data = None
    
    @staticmethod
    def loadConfig():
		# Load the configuration file
		try:
		    Config.data = json.loads( open("Config.json").read() )
		except Exception:
			logging.getLogger("neolib.config").exception("Failed to load configuration file. May not exist or may be corrupted.")
		    return False
		    
		return True
		
	@staticmethod
	def getGroup(groupName):
	    if groupName in Config.data:
			return Config.data[groupName]
	    else:
			logging.getLogger("neolib.config").info("Failed to load group with name " + groupName)
			return False
			
    @staticmethod
    def getConfig(groupName, key):
		if groupName in Config.data:
			if key in Config.data[groupName]:
				return Config.data[groupName][key]
		    else:
				logging.getLogger("neolib.config").info("Failed to load config with group name " + groupName + " and key " + key)
				return False
		else:
			logging.getLogger("neolib.config").info("Failed to load config with group name " + groupName + " and key " + key)
			return False
