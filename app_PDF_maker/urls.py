from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('recursos/', views.recursos, name='recursos'),
    path('requisiciones/', views.requisiciones, name='requisiciones'),
    path('gafetes/', views.gafetes, name='gafetes')
    

]


