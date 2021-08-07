from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import BatchUrl

def download_report(request, pk):
    response = HttpResponse(content_type='application/json')
    bacthUrl = BatchUrl.objects.get(pk=pk)
    response['Content-Disposition'] = 'inline; filename=report_'+str(pk)+'.json'
    response.write(bacthUrl.report)
    return response

def index(request):
    return HttpResponse("Hello, world!")