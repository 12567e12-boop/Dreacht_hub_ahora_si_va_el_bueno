from django.urls import path
from .views import views_requisicion as views_requisicion
from .views import views_gafete as views_gafete


urlpatterns = [
    path('', views_gafete.home, name='home'),
    path('recursos/', views_gafete.recursos, name='recursos'),
    path('requisiciones/', views_requisicion.requisiciones, name='requisiciones'),
    path('gafetes/', views_gafete.gafetes, name='gafetes')


]
