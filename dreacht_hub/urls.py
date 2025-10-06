from django.contrib import admin
from django.urls import path, include



app_name = 'app_PDF_maker'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_PDF_maker.urls')),
]


