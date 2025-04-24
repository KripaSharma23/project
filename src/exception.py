import sys
from src.logger import logging


#function for customizing the error for errors
def error_message_detail(error,error_detail:sys):
    #error_detail-----gives exact information of error
    #exc_value,exc_type,exc_tb=exc_info()
    _,_,exc_tb=error_detail.exc_info()
    fileName=exc_tb.tb_frame.f_code.co_filename
    error_msg="Error occured in pythin script name [{0}]line no [{1}] error message[{2}]".format(fileName,exc_tb.tb_lineno,str(error))
    return error_msg
# Inheritence
class CustomException(Exception):
    def __init__(self,error_msg,error_detail:sys):
        super().__init__(error_msg)
        self.error_msg=error_message_detail(error_msg,error_detail=error_detail)
    def __str__(self):
        return self.error_msg
    

# if __name__=="__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logging.info(" Dvision of zero error")
#         raise CustomException(e,sys)
        
