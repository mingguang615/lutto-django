from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
class RequestAuth(MiddlewareMixin):
    def process_request(self, request):
        # if request.method=="POST":
        #
        #     print('process_request')
        #
        # else:
        #     return HttpResponse('get')
        pass
        # # return HttpResponse('sorry')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        i = 1

        pass
    def process_exception(self, request, exception):

        return HttpResponse(exception)
    def process_response(self, request, response):

        return response
