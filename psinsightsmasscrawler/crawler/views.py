from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .models import BatchUrl

def download_report(request, pk):
    batchUrl = BatchUrl.objects.get(pk=pk)
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'inline; filename=report_'+str(pk)+'.json'
    response.write(batchUrl.report)
    return response

def index(request):
    return HttpResponse("Hello, world!")