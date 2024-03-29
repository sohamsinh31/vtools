from django.contrib import admin
from django.urls import path
from home import views
from . import urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.index,name='home'),
    path("upload/",views.upload,name='upload'),
    path("download/",views.download,name='download'),
    path("download/insta/",views.instagram,name='Instagram'),
    path("download/imagecomp/",views.imagecomp,name='Imagecomp'),
    path("dropbox/",views.dropbox,name='Dropbox'),
    path("image/text/",views.imagetxt,name='Image2text'),
    path("image/edit/",views.imageEdit,name='imageedit'),
    path("api/",views.phpapi,name='api'),
    path('drops/',views.filedownload,name='filedownload')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)