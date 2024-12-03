from django.urls import path
from . import views

urlpatterns = [
    path('estudiantes/listar-estudiantes/', views.get, name='listar_estudiantes'),
]