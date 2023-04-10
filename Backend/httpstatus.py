from enum import Enum

class HttpStatus(Enum):
    ok_200 = 200
    created_201 = 201
    accepted_202 = 202
    no_content_204 = 204
    bad_request_400 = 400
    unauthorized_401 = 401
    forbidden_403 = 403
    notfound_404 = 404
    conflict_409 = 409
    internal_server_error = 500
    not_implemented_501 = 501
    bad_gateway_error = 502
    service_unavailable_503 = 503
    gateway_timeout = 504

    @staticmethod
    def is_success(status_code):
        return 200 <= status_code.value <= 299
    
    @staticmethod
    def is_client_error(status_code):
        return 400 <= status_code.value <= 499
    
    @staticmethod
    def is_server_error(status_code):
        return 500 <= status_code.value <= 599