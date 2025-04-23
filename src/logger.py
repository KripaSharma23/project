import logging
import os
import sys
from datetime import datetime


# ForBasicConfiguration
#created file and folder for our models logs 

log_file=f'{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log'
log_path=os.path.join(os.getcwd(),"LOGS",log_file)

os.makedirs(log_path,exist_ok=True)
# combining both the file and folder
log_file_path=os.path.join(log_path,log_file)

logging.basicConfig(
    filename=log_file_path,
    datefmt='%Y_%m_%d %H:%M:%S',
    format="[%(asctime)s] %(lineno)d %(name)s-%(levelname)s-%(message)s",
    level=logging.INFO
)
logging.debug("error")
if __name__=="__main__":
    logging.info("logging has started")
