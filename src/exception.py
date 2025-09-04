import sys

def error_message_detail(error, error_detail:sys):
    exc_type, exc_obj, exc_tb = error_detail.exc_info()
    error_message = f"""\n\n\nError in python script with name {exc_tb.tb_frame.f_code.co_filename}

    Error Type: {exc_type.__name__}
    Error Message: {error}
    Error Line: {exc_tb.tb_lineno}\n"""
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message
    