from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

import requests

from . import models
from . import forms

def data_view(request):    #pull data from third party rest api
    response = requests.get('http://localhost:8080/api/v1/dataresources/')    #convert reponse data into json
    dataresources = response.json()
    print(dataresources)    
    
    return render(request, "data_view.html", {'dataresources': dataresources})
    pass

def home(request):
    documents = models.Document.objects.all()
    return render(request, 'home.html', { 'documents': documents })

def about(request):    #pull data from third party rest api
    response = requests.get('http://localhost:8080/api/v1/dataresources/')    #convert reponse data into json
    dataresources = response.json()
    print(dataresources)    
    
    return render(request, "about.html", {'dataresources': dataresources})
    pass

def model_form_upload(request):
    if request.method == 'POST':
        form = forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')