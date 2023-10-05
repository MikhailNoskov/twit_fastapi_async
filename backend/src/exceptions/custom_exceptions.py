from fastapi import status


class CustomException(Exception):
    def __init__(self, error_type: str, error_message: str, response_status: status):
        self.result = False
        self.error_type = error_type
        self.error_message = error_message
        self.status = response_status

    def to_dict(self):
        return {
            "status": self.status,
            "result": self.result,
            "error_type": self.error_type,
            "error_message": self.error_message
        }
