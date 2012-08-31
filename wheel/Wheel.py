from neolib.pyamf.remoting.client import RemotingService
from neolib.RegexLib import RegexLib
import logging

class Wheel:
    
    id = 0
    gateway = "http://www.neopets.com/amfphp/gateway.php"
    
    message = ""
    img = ""
    prize = ""
    
    alreadySpun = False
    
    _validIDs = [1, 2, 3, 4, 5, 6]
    _names = {1: 'Wheel of Knowledge', 2: 'Wheel of Excitement', 3: 'Wheel of Mediocrity', 4: 'Wheel of Misfortune', 5: 'Wheel of Monotony', 6: 'Wheel of Extravagence'}
    
    _refs = {1: "", \
            2: "http://images.neopets.com/wheels/wheel_of_excitement_v3_831fbec8f8.swf?quality=high&scale=exactfit&menu=false&allowScriptAccess=always&swLiveConnect=True&wmode=opaque&host_url=www.neopets.com&lang=en", \
            3: "", \
            4: "http://images.neopets.com/wheels/wheel_of_misfortune_v2_3075ced020.swf?quality=high&scale=exactfit&menu=false&allowScriptAccess=always&swLiveConnect=True&wmode=opaque&host_url=www.neopets.com&lang=en", \
            5: "", \
            6: ""}
    
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
        print resp
        # See if we have an error
        if "errmsg" in resp:
            if resp['errmsg'].find("already spun this wheel") != -1:
                self.alreadySpun = True
                return False
            else:
                logging.getLogger("neolib.wheel").info("Wheel spin failed with error message: " + resp['errmsg'])
                return False
        
        # Parse the response
        mats = RegexLib.getMat("wheel", "resp", resp['reply'])
        print mats
        
        # Ensure parse was successful
        if not mats:
            logging.getLogger("neolib.wheel").exception("Failed to parse response with content: " + resp['reply'])
            return False
            
        
        # Set the attributes and return        
        self.message = mats[0][0]
        self.img = mats[0][1]
        self.prize = mats[0][2]
        
        return True
        
        