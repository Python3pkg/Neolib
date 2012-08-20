import json
import os
import Temp
import re

class RegLib:
    regLib = None
    
    @staticmethod
    def loadReg():
        # JSON file is located in the same directory as RegLib.py
        path = os.path.dirname(os.path.abspath(Temp.__file__)) + "/regLib.json"
        
        # Load, read, and parse the JSON into a list
        RegLib.regLib = json.loads( open( path).read() )
    
    @staticmethod
    def getGroup(groupName):
        return RegLib.regLib[groupName]
    
    @staticmethod
    def getReg(groupName, key):
        return RegLib.regLib[groupName][key]
        
    @staticmethod    
    def getMat(groupName, key, str):
        # Find and return all matches for requested regex string in given string
        return re.findall(RegLib.regLib[groupName][key], str)