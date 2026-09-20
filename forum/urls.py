from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('sobre-projeto/', views.sobre_projeto, name='sobre_projeto'),
    path('fale-conosco/', views.fale_conosco, name='fale_conosco'),
]