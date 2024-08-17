from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # URL для домашней страницы
    path('contact/', views.contact, name='contact'),  # URL для страницы с контактной информацией
]
