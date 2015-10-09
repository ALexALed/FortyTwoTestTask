import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import View
from .models import RequestData


class RequestsView(View):

    def get(self, request, *args, **kwargs):
        requests_data = RequestData.objects.all().order_by('-date_time')[0:10]
        new_requests_count = len([new_request for new_request in requests_data
                                  if not new_request.viewed])
        return render_to_response('requests/index.html',
                                  {'object_list': requests_data,
                                   'requests_new': new_requests_count},
                                  context_instance=RequestContext(request))


class RequestsData(View):

    def get(self, request):
        requests_data = RequestData.objects.all().order_by('-date_time')[0:10]
        new_requests_count = len([new_request for new_request in requests_data
                                  if not new_request.viewed])

        requests_to_json = [{'remote_addr': req.remote_addr,
                             'http_request': req.http_request,
                             'date_time':
                                 req.date_time.strftime('%Y-%m-%d %H:%M'),
                             'viewed': req.viewed,
                             'request_id': req.id} for req in requests_data]
        return HttpResponse(json.dumps({'requestsData': requests_to_json,
                                        'requestsNew': new_requests_count}),
                            content_type="application/json")

    def post(self, request):
        if request.is_ajax():
            data = json.loads(request.POST['data'])
            for request_data in data:
                request_object = \
                    RequestData.objects.get(pk=request_data['request_id'])
                request_object.viewed = True
                request_object.save()
            else:
                return HttpResponse(json.dumps({'success': True}),
                                    content_type="application/json")
