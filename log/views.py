from django.shortcuts import render
from django.http import request, HttpResponse
from lxml import etree

from .forms import StudentForm
from .functions import handle_uploaded_file

# Create your views here.

def index(request):
    return HttpResponse("this is index page")

def log(request):
    if request.method == 'POST':
        student = StudentForm(request.POST, request.FILES)
        if student.is_valid():
            handle_uploaded_file(request.FILES['file'])
            parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
            tree = etree.parse('log/upload/xe.xml', parser=parser)
            root = tree.getroot()
            return HttpResponse(root.text)
    else:
        student = StudentForm()
        return render(request, 'log/login.html', {'form':student})  