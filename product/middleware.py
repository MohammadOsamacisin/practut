from datetime import datetime


class BenchmarkMiddleware(object):


    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    def process_request(self, request):
        request._request_time = datetime.now()

    def process_template_response(self, request, response):
        request._request_time = datetime.now()
        response_time = datetime.now() - request._request_time
        response.context_data['response_time'] = response_time
        response.context_data['request_time'] = response_time
        return response