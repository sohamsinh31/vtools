from http.client import HTTPResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from docx2pdf import convert
from django.http import FileResponse
from djangoconvertvdoctopdf.convertor import StreamingConvertedPdf
import aspose.words as aw
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
        fs = FileSystemStorage()
        fs.save(name,uploaded_file)
        print(type(uploaded_file))
        print(type(uploaded_file.read()))
        print(type(str(uploaded_file.read())))
        print("hi")
        pathh = "media/"+uploaded_file.name
        fs.save("output.pdf",convert(pathh,"output.pdf"))
        # doc = aw.Document(uploaded_file)
        # doc.save("Output.pdf")
        # for x in range(len(uploaded_file)):
        #     convert(uploaded_file.read())
        #     convert("{uploaded_file}}", "media\Mine.pdf")
        #     # inst = StreamingConvertedPdf(uploaded_file)
        #     # return inst.stream_content()
        return open("media/output.pdf")
    return render(request,'index.html')