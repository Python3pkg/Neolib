import logging

class HTMLFilter(logging.Filter):
    
    def filter(self, record):
        
        # Do not allow any logs to neolib.html to pass
        if record.name == "neolib.html":
            return False
        else:
            return True