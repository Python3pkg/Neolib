import json
import os
import re
import inspect

class RegexLib:
    lib = None
    
    @staticmethod
    def loadReg():
        # JSON file is located in the same directory as RegexLib.py
        path = os.path.dirname(inspect.getfile(inspect.currentframe())) + "/RegexLib.json"
        
        # Load, read, and parse the JSON into a list
        RegexLib.lib = json.loads( open( path).read() )
    
    @staticmethod
    def getGroup(groupName):
        # Return a group of regex strings
        return RegexLib.lib[groupName]
    
    @staticmethod
    def getReg(groupName, key):
        # Return a specific regex string
        return RegexLib.lib[groupName][key]
        
    @staticmethod    
    def getMat(groupName, key, str):
        # Find and return all matches for requested regex string in given string
        return re.findall(RegexLib.lib[groupName][key], str)