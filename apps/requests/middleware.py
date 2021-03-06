from .models import RequestData


class HttpRequestMiddleware(object):
    def process_request(self, request):
        is_ajax = request.is_ajax()
        if not is_ajax:
            new_http_req = RequestData()
            new_http_req.http_request = request.path_info
            new_http_req.remote_addr = request.META['REMOTE_ADDR']
            new_http_req.save()
