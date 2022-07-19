from datetime import datetime
from multiprocessing import context
from tkinter.messagebox import NO
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from docx2pdf import convert
import os
from os.path import exists
from numpy import product
from pytube import YouTube,streams,helpers
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import instaloader
import shutil
import glob
import io
from PIL.Image import Image
import PIL
from .models import Product
from django.db.models import Q

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
        data = io.BytesIO()
        with open(pathh2,"rb") as fh:
            data.write(fh.read())
        data.seek(0)
        response = HttpResponse(data,content_type='application/pdf')
        response['Content-Disposition'] = "attachment; filename=%s" % finalname
        os.remove(pathh)
        os.remove(pathh2)
        return response
    return render(request,'index.html')

def download(request):
    if request.method == 'POST':
        inp_value = request.POST['download']
        url = YouTube(inp_value)
        video = url.streams.get_highest_resolution()
        filename = video.default_filename
        path=settings.MEDIA2
        video.download(output_path=settings.MEDIA2)
        data = io.BytesIO()
        with open(path+"/"+filename,"rb") as fh:
            data.write(fh.read())
        data.seek(0)
        response = HttpResponse(data,content_type='application/mp4')
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        file_exists = exists(path+"/"+filename)
        if file_exists:
         os.remove(path+"/"+filename)
        return response
    return render(request,'download.html')


def instagram(request):
    if request.method == 'POST':
        inp_value = request.POST['download']
        ig = instaloader.Instaloader()
        dp = inp_value
        filee=dp+".jpg"
        path = "instagram"
        ig.download_profile(dp ,path, profile_pic_only=True)
        files_path = os.path.join(path, '*')
        files = sorted(
           glob.iglob(files_path), key=os.path.getctime, reverse=True) 
        print(files[0])
        directory = dp
        parent = os.getcwd()
        pathh = os.path.join(parent, directory)
        shutil.rmtree(pathh, ignore_errors=True)
        data = io.BytesIO()
        with open(files[0],"rb") as fh:
            data.write(fh.read())
        data.seek(0)
        response = HttpResponse(data,content_type="application/jpg")
        response['Content-Disposition'] = "attachment; filename=%s" % filee
        os.remove(files[0])
        return response
    return render(request,'instadown.html')

def imagecomp(request):
  if request.method == 'POST':
    file = request.FILES['document']
    filename = file.name
    img = PIL.Image.open(file)
    myHeight,myWidth = img.size
    split_tup = os.path.splitext(filename)
    finalname = split_tup[0]
    img = img.resize((myHeight,myWidth),PIL.Image.ANTIALIAS)
    path = "compressor/"+finalname
    img.save(path+"_compressed.jpg")
    data = io.BytesIO()
    with open(path+"_compressed.jpg","rb") as fh:
        data.write(fh.read())
    data.seek(0)
    response = HttpResponse(data,content_type="application/jpg")
    response['Content-Disposition'] = "attachment; filename=%s" % path+"_compressed.jpg"
    os.remove(path+"_compressed.jpg")
    return response
  return render(request,'imagecomp.html')

def dropbox(request):
    a = []
    if request.method=='POST':
        username = request.POST['username']
        if 'download' in request.FILES:
            file = request.FILES['download']
            filename = file.name
            split_tup = os.path.splitext(filename)
            extension = split_tup[1]
            folder = "dropbox/"
            fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
            filename2 = fs.save(file.name, file)
            file_url = folder+filename2
            b=datetime.now()
            c = b.strftime("%m/%d/%Y %H:%M:%S")
            product = Product(
                username=username,
                fileurl=file_url,
                filename=filename2,
                date=c
            )
            product.save()
        query = Product.objects.filter(Q(username=username))
        a.append(query)
    if len(a)==1:
        context={'products':query}
    else:
        context={'products':{'username':''}}
    return render(request,'dropbox.html',context)

def filedownload(request):
    if request.method == 'GET':
        path = request.GET.get('p',None)
        print(path)
        path2 = path.split("/")
        print(path2[1])
        response = HttpResponse(path,content_type="application/force-download")
        response['Content-Disposition'] = "attachment; filename=%s" % path2[1]
        return response
