import os, sys
import shutil
import logging
import time
from TelloBeep.config import conf


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)



def logger(name=__name__):
   
    # created = os.path.getctime(conf.get("LOG_FILE"))
    # year,month,day,hour,minute,second=time.localtime(created)[:-3]


    # new_filename = "%02d%02d%d%02d%02d%02dtellobeep.log"%(second, minute, hour, day, month,year)
    # new_filename = conf["LOG_FILE"].replace("tellobeep.log", new_filename)
    # shutil.move(conf["LOG_FILE"], new_filename)

    logger = logging.getLogger(name)
    # fh = logging.FileHandler(conf['LOG_FILE'])
    fh = logging.StreamHandler(sys.stdout)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(CustomFormatter())



    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    
    return logger


