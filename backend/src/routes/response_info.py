USER_ERROR_RESPONSES = {
    201: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "message": "User successfully registered!"
                }
            }
        }
    },
    403: {
        "description": "CustomException Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Wrong credentials passed"
                }
            }
        }
    },
    404: {
        "description": "CustomException Error",
        "content": {
            "application/json": {
                "example": {
                    "result": "false",
                    "error_type": "users",
                    "error_message": "User not found"
                }
            }
        }
    },
    409: {
        "description": "CustomException Error",
        "content": {
            "application/json": {
                "example": {
                    "result": "false",
                    "error_type": "user",
                    "error_message": "User with supplied api_key exists"
                }
            }
        }
    }
}

MEDIA_ERROR_RESPONSES = {
    403: {
        "description": "CustomException Error",
        "content": {
            "application/json": {
                "example": {
                    "result": "false",
                    "error_type": "media",
                    "error_message": "Access denied"
                }
            }
        }
    }
}
