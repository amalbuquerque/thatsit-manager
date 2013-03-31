# coding: utf8

def handle_uploads_deletes():
    import time
    t = time.ctime()
    logger.debug("Handle Uploads Deletes run at: " + t)
    return t
    
from gluon.scheduler import Scheduler
Scheduler(db, dict(sch1=handle_uploads_deletes))
