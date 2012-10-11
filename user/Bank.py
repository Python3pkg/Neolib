from neolib.exceptions import notEnoughBalance
from neolib.exceptions import parseException
from neolib.exceptions import notEnoughNps
import logging

class Bank:
    
    usr = None
    type = ""
    balance = ""
    yearlyInterest = ""
    dailyInterest = ""
    
    collectedInterest = True
    
    def __init__(self, usr):
        if not usr:
            return
            
        self.usr = usr
            
    def load(self):
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        
        # Verifies account exists
        if not "great to see you again" in pg.content:
            logging.getLogger("neolib.user").info("Could not load user's bank. Most likely does not have an account.")
            logging.getLogger("neolib.html").info("Could not load user's bank. Most likely does not have an account.", {'pg': pg})
            raise noBankAcct
            
        try:
            results = pg.find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
        
            self.type = results[0].text
            self.balance = results[1].text.replace(" NP", "")
            self.interestRate = results[2].text
            self.yearlyInterest = results[3].text
        except Exception:
            logging.getLogger("neolib.user").exception("Could not parse user's bank details.")
            logging.getLogger("neolib.html").info("Could not parse user's bank details.", {'pg': pg})
            raise parseException
        
        # Checks if interest has been collected
        if not "not be able to collect" in pg.content and not "have already collected" in page.content:
            try:
                self.dailyInterest = pg.find("input", {'value': 'interest'}).find_next_sibling('input')['value'].split("(")[1].split(" NP)")[0]
                self.collectedInterest = False
            except Exception:
                logging.getLogger("neolib.user").exception("Could not parse user's bank daily interest.")
                logging.getLogger("neolib.html").info("Could not parse user's bank daily interest.", {'pg': pg})
                raise parseException
    
    def deposit(self, amount):
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        
        if self.usr.nps < int(amount):
            raise notEnoughNps
            
        pg = self.usr.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'deposit', 'amount': str(amount)})
        
        # Success redirects to bank page
        if "It's great to see you again" in pg.content:
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to deposit NPs for unknown reason. User NPs: " + str(self.usr.nps) + ". Amount: " + str(amount))
            logging.getLogger("neolib.html").info("Failed to deposit NPs for unknown reason.", {'pg': pg})
            return False
        
        self.updateBalance()
            
    def withdraw(self, amount):
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        
        try:
            results = pg.find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
            self.balance = results[1].text.replace(" NP", "")
        except Exception:
            logging.getLogger("neolib.user").exception("Could not parse user's bank balance.")
            logging.getLogger("neolib.html").info("Could not parse user's bank balance.", {'pg': pg})
        
        if int(amount) > int(self.balance.replace(",", "")):
            raise notEnoughBalance
            
        pg = self.usr.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'withdraw', 'amount': str(amount)}, usePin = True)
        
        # Success redirects to bank page
        if "It's great to see you again" in pg.content:
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to withdraw NPs for unknown reason. User NPs: " + str(self.usr.nps) + ". Amount: " + str(amount))
            logging.getLogger("neolib.html").info("Failed to withdraw NPs for unknown reason.", {'pg': pg})
            return False
        
        self.updateBalance()
            
    def collectInterest(self):
        if self.collectedInterest:
            return False
            
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        pg = self.usr.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'interest'})
        
        # Success redirects to bank page
        if "It's great to see you again" in pg.content:
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to collect daily interest for unknown reason.")
            logging.getLogger("neolib.html").info("Failed to collect daily interest for unknown reason.", {'pg': pg})
            return False
        
        
    def updateBalance(self):
        pg = self.usr.getPage("http://www.neopets.com/bank.phtml")
        
        try:
            results = pg.find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
            self.balance = results[1].text.replace(" NP", "")
        except Exception:
            logging.getLogger("neolib.user").exception("Could not parse user's bank balance.")
            logging.getLogger("neolib.html").info("Could not parse user's bank balance.", {'pg': pg})
