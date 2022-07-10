from http.client import HTTPResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from docx2pdf import convert
from django.http import FileResponse
import os
from pytube import YouTube,streams,helpers
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
        finalname = split_tup[0]+".pdf"
        fs = FileSystemStorage()
        fs.save(name,uploaded_file)
        pathh = "media/"+uploaded_file.name
        pathh2="media/"+finalname
        convert(pathh,pathh2)
        if convert:
            print("success")
        else:
            print("kuchh or try karo bhai")
        return FileResponse(open(pathh2, 'rb'), content_type='application/pdf')
    return render(request,'index.html')

def download(request):
    if request.method == 'POST':
        inp_value = request.POST['download']
        print(inp_value)
        url = YouTube(inp_value)
        video = url.streams.get_highest_resolution()
        filename = video.default_filename
        ffpath = video.get_file_path(output_path=None)
        video.download()
        with open(filename,"rb") as fh:
            data = fh.read()
        response = HttpResponse(data, content_type='video/mp4')
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
    return render(request,'download.html',context = {'filename': filename})