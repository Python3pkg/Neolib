import json
import os
import re
import inspect
import logging

class RegexLib:
    lib = None
    
    @staticmethod
    def loadReg():
        # JSON file is located in the same directory as RegexLib.py
        path = os.path.dirname(inspect.getfile(inspect.currentframe())) + "/RegexLib.json"
        
        # Load, read, and parse the JSON into a list
        try:
            RegexLib.lib = json.loads( open( path ).read() )
        except Exception:
			logging.getLogger("neolib.regex").exception("Failed to load and parse regex from local file: " + path)
			return False
			
        return True
    
    @staticmethod
    def getGroup(groupName):
        # Return a group of regex strings
        if groupName in RegexLib.lib:
			return RegexLib.lib[groupName]
        else:
			logging.getLogger("neolib.regex").info("Failed to get group with name: " + groupName)
			return False
    
    @staticmethod
    def getReg(groupName, key):
        # Return a specific regex string
        if groupName in RegexLib.lib:
            if key in RegexLib.lib[groupName]:
                return RegexLib.lib[groupName][key]
            else:
                logging.getLogger("neolib.regex").info("Failed to get Regex string in group " + groupName + " with key " + key)
                return False
        else:
			logging.getLogger("neolib.regex").info("Failed to get Regex string in group " + groupName + " with key " + key)
			return False
        
    @staticmethod    
    def getMat(groupName, key, str):
        if not RegexLib.getReg(groupName, key):
            return False
        # Find and return all matches for requested regex string in given string
        return re.findall(RegexLib.lib[groupName][key], str)
