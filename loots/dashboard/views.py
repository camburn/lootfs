from django.shortcuts import render

# Create your views here.


def configuration_view(request):

    html = '<html><body><h1>Admin View</h1><p>Testing the view</p></body></html'

    return HttpResponse(html)