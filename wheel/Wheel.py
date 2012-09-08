from neolib.pyamf.remoting.client import RemotingService
from neolib.bs4 import BeautifulSoup
import logging

class Wheel:
    
    # Wheel ID
    id = 0
    
    # Gateway to communicate with
    gateway = "http://www.neopets.com/amfphp/gateway.php"
    
    
    # Wheel message
    message = ""
    
    # Wheel prize image
    img = ""
    
    # Wheel prize name
    prize = ""
    
    
    # Whether or not the wheel has already been spun
    alreadySpun = False
    
    
    # List of all valid wheel IDs
    _validIDs = [1, 2, 3, 4, 5, 6]
    
    # Dictionary converting IDs to names
    _names = {1: 'Wheel of Knowledge', 2: 'Wheel of Excitement', 3: 'Wheel of Mediocrity', 4: 'Wheel of Misfortune', 5: 'Wheel of Monotony', 6: 'Wheel of Extravagence'}
    
    
    # Dictionary converting IDs to referrers
    _refs = {1: "http://images.neopets.com/wheels/wheel_of_knowledge_v2_731eafc8f8.swf?quality=high&scale=exactfit&menu=false&allowScriptAccess=always&swLiveConnect=True&wmode=opaque&host_url=www.neopets.com&lang=en", \
            2: "http://images.neopets.com/wheels/wheel_of_excitement_v3_831fbec8f8.swf?quality=high&scale=exactfit&menu=false&allowScriptAccess=always&swLiveConnect=True&wmode=opaque&host_url=www.neopets.com&lang=en", \
            3: "http://images.neopets.com/wheels/wheel_of_mediocrity_v2_c4ed41eb31.swf?quality=high&scale=exactfit&menu=false&allowScriptAccess=always&swLiveConnect=True&wmode=opaque&host_url=www.neopets.com&lang=en", \
            4: "http://images.neopets.com/wheels/wheel_of_misfortune_v2_3075ced020.swf?quality=high&scale=exactfit&menu=false&allowScriptAccess=always&swLiveConnect=True&wmode=opaque&host_url=www.neopets.com&lang=en", \
            5: "http://images.neopets.com/wheels/wheel_of_monotony_v2_380e3dbdad.swf?quality=high&scale=exactfit&menu=false&allowScriptAccess=always&swLiveConnect=True&wmode=opaque&host_url=www.neopets.com&lang=en", \
            6: "http://images.neopets.com/wheels/wheel_of_extravagance_v1_5dd2d07006.swf?quality=high&scale=exactfit&menu=false&allowScriptAccess=always&swLiveConnect=True&wmode=opaque&host_url=www.neopets.com&lang=en"}
    
    def __init__(self, wheelID):
        self.id = wheelID
        
    def spinWheel(self, usr):
        # Verify a valid ID was given
        if not self.id in self._validIDs:
            logging.getLogger("neolib.wheel").info("Failed to spin wheel with ID: " + str(self.id))
            return False
        
        # Create a client for the gateway
        client = RemotingService(self.gateway, referer = self._refs[self.id])

        # Ensure we send cookies
        client.addHTTPHeader('Cookie', usr.cookieJar.getCookies())

        # Obtain the WheelService and spin the wheel
        service = client.getService('WheelService')
        resp = service.spinWheel(str(self.id))
        
        # See if we have an error
        if "errmsg" in resp:
            if resp['errmsg'].find("already spun this wheel") != -1:
                self.alreadySpun = True
                return False
            else:
                logging.getLogger("neolib.wheel").info("Wheel spin failed with error message: " + resp['errmsg'])
                return False
        
        # Parse the response
        p = BeautifulSoup(resp['reply']) 
        
        # Set the attributes and return
        self.prize = p.img.text      
        self.message = p.center.text.replace(self.prize, "")
        self.img = p.img['src']
        
        return True
        
        