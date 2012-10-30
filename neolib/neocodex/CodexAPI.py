""":mod:`Page` -- Provides an interface for accessing Neocodex's Item Database

.. module:: Page
   :synopsis: Provides an interface for accessing Neocodex's Item Database
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.neocodex.blowfish import Blowfish
import requests
import urllib
import random
import json

class CodexAPI:
    
    """Provides an interface for accessing Neocodex's Item Database
    
    Neocodex, a Neopets cheating community, offers an extensive item
    database which has an API intended to be used by program developers.
    This class provides an interface for properly communicating with that
    API. Please note you must set your API key and ID for successful API
    queries. 
    
    Attributes
       key (str) -- Your Neocodex API key
       id (str) -- Your Neocodex API ID
        
    Example
       >>> CodexAPI.setAuth("id", "key")
       >>> CodexAPI.searchOne("name", "Green Apple")
       {u'shop_price': 461, u'price': 705, u'name': u'Green Apple', u'object_id': 1}

    """
    
    key = ""
    keyID = 0
    
    @staticmethod
    def setAuth(keyID, key):
        """ Sets the API key and ID for making requests
           
        Parameters:
           keyID (str) -- API Key ID
           key (str) -- API Key
        """
        CodexAPI.keyID = keyID
        CodexAPI.key = key
    
    def priceItems(items):
        """ Takes a list of Item objects and returns a list of Item objects with respective prices modified
        
        Uses the given list of item objects to formulate a query to the item database. Uses the returned
        results to populate each item in the list with its respective price, then returns the modified list.
           
        Parameters:
           items (list[Item]) -- List of items to price
           
        Returns
           list[Item] - Priced list of items
        """
        retItems = []
        sendItems = []
        for item in items:
            sendItems.append(item.name)
        
        resp = CodexAPI.searchMany(sendItems)
        
        for respItem in resp:
            retItems[respItem['name']].price = respItem['price']
            
        return retItems
    
    @staticmethod
    def searchOne(search, text):
        """ The API searchOne function. See API documentation for further explanation.
           
        Parameters:
           search (str) -- Type of search
           text (str) -- Text to search for
           
        Returns
           dict - API search results
        """
        return CodexAPI._callAPI({'do': 'itemdb_read_one', 'search': search, 'value': text})
    
    @staticmethod
    def searchMany(items):
        """ The API searchMany function. See API documentation for further explanation.
           
        Parameters:
           items (list) -- Items to search for
           
        Returns
           dict - API search results
        """
        return CodexAPI._callAPI({'do': 'itemdb_read_many', 'items': items})
        
    @staticmethod
    def _callAPI(data):
        # Compile the items for the api in a random order.
        send_list = []
        for key, value in random.sample(data.items(), len(data)):
            # Lists and dicts cannot be transferd as str, use simplejson.dumps
            if isinstance(value, (list, dict)):
                value = json.dumps(value)
            
            send_list.append("%s=%s" % (key, urllib.quote(str(value))))
            
        send_encode = "&".join(send_list)
        
        # Encrypt the output using our key.
        #bf = Blowfish(CodexAPI.key)
        #bf.initCTR()
        #send_data = bf.encryptCTR(str(send_encode)).encode('hex').upper()
        
        # Send and recieve the data
        r = requests.post("http://djangoapi.neocodex.us/api/do/?key=%s" % CodexAPI.key, data=send_encode)
        return r.json
