import logging
from datetime import datetime

class HTMLHandler(logging.Handler):
         
    def emit(self, record):
        # Create a unique file name to identify where this HTML source is coming from
        fileName = datetime.today().strftime("Neolib %Y-%m-%d %H-%M-%S ") + record.module + ".html"
        
        # Sometimes module may encase the text with < > which is an invalid character for a file name
        fileName = fileName.replace("<", "").replace(">", "")
        
        # Grab the pg
        pg = record.args['pg']
        
        # Format a log message that details the page
        ret = "Message: " + record.msg + "\nLine Number: " + str(record.lineno) + "\nURL: " + str(pg.url) + "\nPost Data: " + str(pg.postData) + "\nCookies" + str(pg.intCookies) + "\nAdditional Vars: " + str(pg.vars)
        ret += "\n\n\n" + pg.header.content + "\n\n" + pg.content
        
        # Write the file
        f = open(fileName, "w")
        f.write(ret)
        f.close()
        
        