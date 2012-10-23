from neolib.http.Page import Page
import threading
import datetime
import time

class NST(threading.Thread):
    curTime = None
    running = False
    
    inst = None
    
    @staticmethod
    def initialize():
        NST.running = True
        pg = Page("http://www.neopets.com/")
        
        curtime = pg.find("td", {'id': 'nst'}).text
        NST.curTime = datetime.datetime.strptime(curtime.replace(" NST", ""), "%I:%M:%S %p") + datetime.timedelta(0,2)
        
        NST.inst = NST()
        NST.daemon = True # Ensures the thread is properly destroyed when the master program terminates
        NST.inst.start()
        
    @staticmethod
    def time():
        return NST.curTime
        
    def run(self):
        while NST.running:
            NST.curTime = NST.curTime + datetime.timedelta(0,1)
            time.sleep(1)
