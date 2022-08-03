from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from docx2pdf import convert
import os
from os.path import exists
from numpy import product
from pytube import YouTube,helpers,streams
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
import string
import random
import pytesseract
from gtts.tts import gTTS
import pyttsx3

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
    return render(request,'upload.html')

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
        response = HttpResponse(data,content_type='video/mp4')
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
        #print(files[0])
        directory = dp
        parent = os.getcwd()
        pathh = os.path.join(parent, directory)
        shutil.rmtree(pathh, ignore_errors=True)
        data = io.BytesIO()
        with open(files[0],"rb") as fh:
            data.write(fh.read())
        data.seek(0)
        response = HttpResponse(data,content_type="image/jpg")
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
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        def generate_random_password():
            random.shuffle(characters)
            password = []
            for i in range(10):
                password.append(random.choice(characters))
            random.shuffle(password)
            return "".join(password)
        username = generate_random_password()
        if 'username' in request.POST:
            if request.POST['username'] != '':
                username = request.POST['username']
        if 'username2' in request.POST:
            if request.POST['username2'] != '':
                username = request.POST['username2']
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
    if request.method == 'POST':
        try:
            path = request.POST['fileurl']
            file_exists = exists(path)
            if file_exists:
                path2 = path.split("/")
                data = io.BytesIO()
                with open(path,"rb") as fh:
                    data.write(fh.read())
                data.seek(0)
                response = HttpResponse(data,content_type="image/jpg")
                response['Content-Disposition'] = "attachment; filename=%s" % path2[1]
                return response
            else:
                return HttpResponse("<h3>file not found your time limit is over</h3>")

        except:
            return HttpResponse("<h3>file not found your time limit is over</h3>")
def imagetxt(request):
    import PIL.Image
    a=[]
    if request.method == 'POST':
        if 'image' in request.FILES:
            image = request.FILES['image']
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(PIL.Image.open(image), lang="eng")
            language = 'en'
            myobj = gTTS(text=text, lang=language, slow=False)
            data = io.BytesIO()
            a.append(text)
    if len(a)>0:
        context={'text':a[0],'audio':a[0]}
    else:
        context={'text':"none"}
    return render(request,'image2txt.html',context)