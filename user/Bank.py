from neolib.exceptions import parseException
from neolib.exceptions import notEnoughBalance
from neolib.exceptions import notEnoughNps
import logging

class Bank:
    
    owner = None
    
    type = ""
    balance = ""
    interestRate = ""
    yearlyInterest = ""
    dailyInterest = ""
    
    collectedInterest = True
    
    def __init__(self, usr):
        # Ensure we got a user
        if not usr:
            return
            
        self.owner = usr
            
        # Load the bank page
        pg = usr.getPage("http://www.neopets.com/bank.phtml")
        
        # Ensure an account exists
        if not pg.content.find("great to see you again"):
            logging.getLogger("neolib.user").info("Could not load user's bank. Most likely does not have an account. Source: \n" + pg.content + "\n\n\n")
            raise noBankAcct
            
        # Parse bank details
        results = pg.getParser().find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
        
        self.type = results[0].text
        self.balance = results[1].text.replace(" NP", "")
        self.interestRate = results[2].text
        self.yearlyInterest = results[3].text
        
        # See if interest has or has not been collected
        if pg.content.find("not be able to collect") == -1:
            self.dailyInterest = pg.getParser().find_all("td", "contentModuleHeaderAlt")[2].parent.parent.input['value'].split("(")[1].replace(" NP)", "")
            self.collectedInterest = False
            
    
    def deposit(self, amount):
        # Load the bank page
        pg = self.owner.getPage("http://www.neopets.com/bank.phtml")
        
        # Update current user NPs
        self.owner.updateNps(pg)
        
        # Ensure we're not depositing more than we have
        if self.owner.nps < int(amount):
            raise notEnoughNps
            
        pg = self.owner.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'deposit', 'amount': str(amount)})
        
        # Ensure there were no errors
        if pg.header.vars['Location'].find("bank.phtml") != -1:
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to deposit NPs for unknown reason. User NPs: " + str(self.owner.nps) + ". Amount: " + str(amount) + ". Source: \n" + pg.content + "\n\n\n")
            return False
            
        # Reload the bank page
        pg = self.owner.getPage("http://www.neopets.com/bank.phtml")
        
        # Update current balance
        results = pg.getParser().find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
        self.balance = results[1].text.replace(" NP", "")
            
    def withdraw(self, amount):
        # Load the bank page
        pg = self.owner.getPage("http://www.neopets.com/bank.phtml")
        
        # Update current balance
        results = pg.getParser().find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
        self.balance = results[1].text.replace(" NP", "")
        
        # Ensure we're not withdrawing more than we have
        if int(amount) > int(self.balance):
            raise notEnoughBalance
            
        pg = self.owner.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'withdraw', 'amount': str(amount)})
        
        # Ensure there were no errors
        if pg.header.vars['Location'].find("bank.phtml") != -1:
            return True
        else:
            logging.getLogger("neolib.user").info("Failed to deposit NPs for unknown reason. User NPs: " + str(self.owner.nps) + ". Amount: " + str(amount) + ". Source: \n" + pg.content + "\n\n\n")
            return False
            
        # Reload the bank page
        pg = self.owner.getPage("http://www.neopets.com/bank.phtml")
        
        # Update current balance
        results = pg.getParser().find(text = "Account Type:").parent.parent.parent.find_all("td", align="center")
        self.balance = results[1].text.replace(" NP", "")
            
    def collectInterest(self):
        # Make sure we have not already collected interest
        if self.collectedInterest:
            return False
        
        # Go to bank page
        pg = usr.getPage("http://www.neopets.com/bank.phtml")
        
        # Grab the interest
        pg = usr.getPage("http://www.neopets.com/process_bank.phtml", {'type': 'interest'})
        
        f = open("test.html", "w")
        f.write(pg.content)
        f.close()