""":mod:`exceptions` -- Provides all exceptions for Neolib

.. module:: exceptions
   :synopsis: Provides all exceptions for Neolib
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

# General
class parseException(Exception):
    pass

class invalidUser(Exception):
    pass
    
class invalidType(Exception):
    pass
    
class invalidMethod(Exception):
    pass
    
class neopetsOfflineException(Exception):
    pass
    
    
# HTTP
class HTTPException(Exception):
    pass

class invalidProxy(Exception):
    pass
    
class browserNotInstalled(Exception):
    pass
    
class noCookiesForDomain(Exception):
    pass
    
    
# User
class logoutException(Exception):
    pass

class notEnoughBalance(Exception):
    pass
    
class notEnoughNps(Exception):
    pass
    
    
    
# Daily
class dailyAlreadyDone(Exception):
    pass
    
class snowagerAwake(Exception):
    pass
    
class marrowNotAvailable(Exception):
    pass

class invalidDaily(Exception):
    pass
    
    
    
# Inventory
class emptyInventory(Exception):
    pass
    
    
    
# Shop
class invalidSearch(Exception):
    pass
    
class shopWizBanned(Exception):
    time = ""
    pass

class invalidShop(Exception):
    pass
    
class emptyShop(Exception):
    pass
    
class activeQuest(Exception):
    pass
class failedOCR(Exception):
    pass
    
# Quest
class questTooExpensive(Exception):
    pass
    
class UBItemException(Exception):
    pass
    
class questLimitException(Exception):
    pass
    
    
