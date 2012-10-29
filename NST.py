""":mod:`SDB` -- Provides an interface for tracking local NST

.. module:: SDB
   :synopsis: Provides an interface for tracking local NST
.. moduleauthor:: Joshua Gilman <joshuagilman@gmail.com>
"""

from neolib.http.Page import Page
import threading
import datetime
import time

class NST(threading.Thread):
    
    """Provides an interface for tracking local NST
    
    Subclasses threading.Thread to provide the ability to create an
    independant thread which loads NST time upon initialization and 
    proceeds to keep track of current NST time second by second. 
    
    
    Attributes
       curTime (datetime) -- Current NST time
       running (bool) -- Whether or not global thread is running
       inst (NST) -- Global NST instance running
        
    Example
       >>> NST.initialize()
       >>> NST.time()
       <datetime ...>
    """
    
    curTime = None
    running = False
    
    inst = None
    
    @staticmethod
    def initialize():
        """ Initializes the global NST instance with the current NST and begins tracking
        """
        NST.running = True
        pg = Page("http://www.neopets.com/")
        
        curtime = pg.find("td", {'id': 'nst'}).text
        NST.curTime = datetime.datetime.strptime(curtime.replace(" NST", ""), "%I:%M:%S %p") + datetime.timedelta(0,2)
        
        NST.inst = NST()
        NST.daemon = True # Ensures the thread is properly destroyed when the master thread terminates
        NST.inst.start()
        
    @staticmethod
    """ Returns current NST
    
    Returns
       datetime - Current NST
    """
    def time():
        return NST.curTime
        
    def run(self):
        while NST.running:
            NST.curTime = NST.curTime + datetime.timedelta(0,1)
            time.sleep(1)
