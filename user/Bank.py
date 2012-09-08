from neolib.exceptions import notEnoughBalance
from neolib.exceptions import parseException
from neolib.exceptions import notEnoughNps
import logging

class Bank:
    
    # The User who owns the bank
    owner = None
    
    # Type of bank account
    type = ""
    
    # Balance
    balance = ""
    
    # Interest rate
    interestRate = ""
    
    # Total interest in a year
    yearlyInterest = ""
    
    # Total interest in a day
    dailyInterest = ""
    
    
    # Whether or not daily interest has been collected
    collectedInterest = True
    
    def __init__(self, usr):
        # Ensure we got a user
        if not usr:
            return
            
        # Set the user
        self.owner = usr
            
        # Load the bank page
        pg = usr.getPage("http://www.neopets.com/bank.phtml")
        
        # Ensure an account exists
        if not pg.content.find("great to see you again"):
            logging.getLogger("neolib.user").info("Could not load user's bank. Most likely does not have an account.")
            logging.getLogger("neolib.html").info("Could not load user's bank. Most likely does not have an account.", {'pg': pg})
            raise noBankAcct
            
        # Parse bank details
        try:
            results = pg.getParser().find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
        
            self.type = results[0].text
            self.balance = results[1].text.replace(" NP", "")
            self.interestRate = results[2].text
            self.yearlyInterest = results[3].text
        except Exception:
            logging.getLogger("neolib.user").exception("Could not parse user's bank details.")
            logging.getLogger("neolib.html").info("Could not parse user's bank details.", {'pg': pg})
            raise parseException
        
        # See if interest has or has not been collected
        if pg.content.find("not be able to collect") == -1:
            try:
                self.dailyInterest = pg.getParser().find_all("td", "contentModuleHeaderAlt")[2].parent.parent.input['value'].split("(")[1].replace(" NP)", "")
                self.collectedInterest = False
            except Exception:
                logging.getLogger("neolib.user").exception("Could not parse user's bank daily interest.")
                logging.getLogger("neolib.html").info("Could not parse user's bank daily interest.", {'pg': pg})
                raise parseException
            
    
    def deposit(self, amount):
        # Load the bank page
        pg = self.owner.getPage("http://www.neopets.com/bank.phtml")
        
        # Ensure we're not depositing more than we have
        if self.owner.nps < int(amount):
            raise notEnoughNps
            
        # Deposit the amount
        pg = self.owner.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'deposit', 'amount': str(amount)})
        
        # Ensure there were no errors
        if pg.header.vars['Location'].find("bank.phtml") != -1:
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to deposit NPs for unknown reason. User NPs: " + str(self.owner.nps) + ". Amount: " + str(amount))
            logging.getLogger("neolib.html").info("Failed to deposit NPs for unknown reason.", {'pg': pg})
            return False
        
        # Update current balance
        self.updateBalance()
            
    def withdraw(self, amount):
        # Load the bank page
        pg = self.owner.getPage("http://www.neopets.com/bank.phtml")
        
        # Update current balance
        try:
            results = pg.getParser().find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
            self.balance = results[1].text.replace(" NP", "")
        except Exception:
            logging.getLogger("neolib.user").exception("Could not parse user's bank balance.")
            logging.getLogger("neolib.html").info("Could not parse user's bank balance.", {'pg': pg})
        
        # Ensure we're not withdrawing more than we have
        if int(amount) > int(self.balance):
            raise notEnoughBalance
            
        # Withdraw the amount
        pg = self.owner.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'withdraw', 'amount': str(amount)})
        
        # Ensure there were no errors
        if pg.header.vars['Location'].find("bank.phtml") != -1:
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to withdraw NPs for unknown reason. User NPs: " + str(self.owner.nps) + ". Amount: " + str(amount))
            logging.getLogger("neolib.html").info("Failed to withdraw NPs for unknown reason.", {'pg': pg})
            return False
        
        # Update current balance
        self.updateBalance()
            
    def collectInterest(self):
        # Make sure we have not already collected interest
        if self.collectedInterest:
            return False
        
        # Go to bank page
        pg = usr.getPage("http://www.neopets.com/bank.phtml")
        
        # Grab the interest
        pg = usr.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'interest'})
        
        # Ensure there were no errors
        if pg.header.vars['Location'].find("bank.phtml") != -1:
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to collect daily interest for unknown reason.")
            logging.getLogger("neolib.html").info("Failed to collect daily interest for unknown reason.", {'pg': pg})
            return False
        
        
    def updateBalance(self):
        # Load the bank page
        pg = self.owner.getPage("http://www.neopets.com/bank.phtml")
        
        # Update current balance
        try:
            results = pg.getParser().find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
            self.balance = results[1].text.replace(" NP", "")
        except Exception:
            logging.getLogger("neolib.user").exception("Could not parse user's bank balance.")
            logging.getLogger("neolib.html").info("Could not parse user's bank balance.", {'pg': pg})