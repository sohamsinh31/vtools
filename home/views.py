from http.client import HTTPResponse
from typing import final
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from docx2pdf import convert
from django.http import FileResponse
from djangoconvertvdoctopdf.convertor import StreamingConvertedPdf
import PyPDF2
import os
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    if request.method == 'POST':
        uploaded_file=request.FILES['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
    return render(request,'index.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file=request.FILES['document']
        name=uploaded_file.name
        split_tup = os.path.splitext(name)
        print(split_tup)
        file_name = split_tup[0]
        finalname = split_tup[0]+".pdf"
        file_extension = split_tup[1]
        fs = FileSystemStorage()
        fs.save(name,uploaded_file)
        print(type(uploaded_file))
        print(type(uploaded_file.read()))
        print(type(str(uploaded_file.read())))
        pathh = "media/"+uploaded_file.name
        pathh2="media/"+finalname
        convert(pathh,pathh2)
        if convert:
            print("success")
        else:
            print("kuchh or try karo bhai")
        return FileResponse(open(pathh2, 'rb'), content_type='application/pdf')
    return render(request,'index.html')