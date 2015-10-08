from django.shortcuts import render_to_response
from django.views.generic import View
from .models import RequestData


class RequestsView(View):

    def get(self, request, *args, **kwargs):
        return render_to_response('requests/index.html',
                                  {'object_list': RequestData.objects.all().order_by('-date_time')[0:10],
                                   'new_requests': RequestData.objects.filter(viewed=False).count()})


    def post(self):
        pass