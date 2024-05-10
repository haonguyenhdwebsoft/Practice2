from .models import APIResponse

def get_response_format(data_format, status_code, success=True):
    api_response = APIResponse(status_code=status_code, success=success, data=data_format)
    return api_response.get_response()