import logging
from datetime import datetime


def current_time():
    """
    Get current time
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getLogger(name):
    """
    Create log by name with stream handler
    """
    log = logging.getLogger(name)

    # Create a console handler
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    log.setLevel(logging.INFO)
    log.addHandler(ch)

    return log
