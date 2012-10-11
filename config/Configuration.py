from collections import MutableMapping
from neolib.http.Page import Page
import logging
import json

class Configuration(MutableMapping):
    path = "config.json"
    __config = None
    
    def __init__(self, data):
        self.__dict__ = data

    def write(self):
        Configuration.__writeConfig()

    def addSection(self, name):
        self.__dict__[name] = Configuration({})
        
    def toDict(self):
        return self.__dict__
    
    def __getitem__(self, key):
        return self.__dict__[key]
        
    def __setitem__(self, key, value):
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
        try:
            f = open(Configuration.path, 'r')
            data = f.read()
            f.close()
        except Exception:
            Configuration.__createDefault()
            return True
            
        try:
            Configuration.__config = Configuration(json.loads(data))
            Configuration.__makeConfig(Configuration.__config)
        except Exception as e:
            logging.getLogger("neolib.config").exception("Failed to read configuration file: " + Configuration.path)
            return False
            
        return True
        
    @staticmethod
    def reload():
        return Configuration.initialize()
        
    @staticmethod
    def getConfig():
        return Configuration.__config
    
    @staticmethod
    def loaded():
        return bool(Configuration.__config)
        
    @staticmethod
    def __writeConfig():
        try:
            f = open(Configuration.path, 'w')
            f.write(json.dumps(Configuration.__makeDict(Configuration.__config)))
            f.close()
            
            Configuration.__makeConfig(Configuration.__config)
        except Exception:
            logging.getLogger("neolib.config").exception("Failed to write configuration file: " + Configuration.path + "\n With content: \n" + Configuration.__makeDict(Configuration.__config))
            return False
            
        return True

    @staticmethod
    def __makeDict(c):
        for item in c:
            if isinstance(c[item], MutableMapping):
                Configuration.__makeDict(c[item])
                c.__dict__[item] = dict(c[item])
        
        return dict(c)

    @staticmethod
    def __makeConfig(c):
        if not isinstance(c, dict) and not isinstance(c, MutableMapping): return
        if len(c) <= 0 and not isinstance(c, MutableMapping): 
            c = Configuration(c)
            return
            
        for key in c:
            if isinstance(c[key], dict):
                c[key] = Configuration(c[key])
                Configuration.__makeConfig(c[key])

    @staticmethod
    def __createDefault():
        default = {'core': {'HTTPHeaders': Page._defaultVars, 'Debug': 'False'}, 'users': {}}
        
        try:
            f = open(Configuration.path, 'w')
            f.write(json.dumps(default, sort_keys = True, indent = 4))
            f.close()
        except Exception:
            logging.getLogger("neolib.config").exception("Failed to create configuration file: " + path)
            return False
            
        Configuration.__config = Configuration(default)
        Configuration.__makeConfig(Configuration.__config)
                
