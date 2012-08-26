class Config:
    test = None
    
    def __init__(self):
        if not Config.test:
            Config.test = "test"
            # Some comments
            # Some comments