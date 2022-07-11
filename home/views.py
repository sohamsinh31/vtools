from http.client import HTTPResponse
import profile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from docx2pdf import convert
from django.http import FileResponse
import os
from pytube import YouTube,streams,helpers
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import instaloader
import shutil
import glob
import io

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
        path=settings.MEDIA2
        print(settings.MEDIA2)
        video.download(output_path=settings.MEDIA2)
        data = io.BytesIO()
        with open(path+"/"+filename,"rb") as fh:
            data.write(fh.read())
        data.seek(0)
        response = HttpResponse(data,content_type='application/mp4')
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        os.remove(path+"/"+filename)
        return response
    return render(request,'download.html')

def instagram(request):
    if request.method == 'POST':
        inp_value = request.POST['download']
        ig = instaloader.Instaloader()
        dp = inp_value
        filee=dp+".jpg"
        path ="instagram"
        ig.download_profile(dp ,path, profile_pic_only=True)
        files_path = os.path.join(path, '*')
        files = sorted(
           glob.iglob(files_path), key=os.path.getctime, reverse=True) 
        print(files[0])
        directory = dp
        parent = os.getcwd()
        path = os.path.join(parent, directory)
        shutil.rmtree(path, ignore_errors=False)
        data = io.BytesIO()
        with open(files[0],"rb") as fh:
            data.write(fh.read())
        data.seek(0)
        response = HttpResponse(data,content_type="application/jpg")
        response['Content-Disposition'] = "attachment; filename=%s" % filee
        os.remove(files[0])
        return response
    return render(request,'instadown.html')
