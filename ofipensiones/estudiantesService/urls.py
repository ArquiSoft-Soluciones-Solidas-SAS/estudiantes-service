from django.urls import path
from . import views

urlpatterns = [
    path('listar-estudiantes/', views.get, name='listar_estudiantes'),
]