import sys , os

class SensorException(Exception):

    def __init__(self , message : str , error_detail : sys):
        super().__init__(message)
        self.message = message
        self.error_detail = error_detail

    def __str__(self) -> str:
        return f"Error Message : {self.message} \n Error Detail : {self.error_detail.exc_info()[2].tb_frame.f_code.co_filename} \n Line Number : {self.error_detail.exc_info()[2].tb_lineno}" 
    