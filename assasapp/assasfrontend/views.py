# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

import requests# Create your views here.

def dataresources(request):    #pull data from third party rest api
    response = requests.get('http://localhost:8080/api/v1/dataresources/')    #convert reponse data into json
    dataresources = response.json()
    print(dataresources)    
    
    return render(request, "dataresources.html", {'dataresources': dataresources})
    pass

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')
