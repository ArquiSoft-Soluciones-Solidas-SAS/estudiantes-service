import factory
from bson import ObjectId
from factory import Faker
from faker.generator import random
from pymongo import MongoClient
from django.conf import settings
import requests
import json
from .models import Estudiante
import factory.django
from factory.mongoengine import MongoEngineFactory
from faker_education import SchoolProvider


class EstudianteFactory(MongoEngineFactory):
    class Meta:
        model = Estudiante

    nombreEstudiante = Faker('name')
    codigoEstudiante = Faker('ean13')


def obtener_cursos_embebidos():
    """
    Conecta a la base de datos remota y obtiene los cursos embebidos dentro de las instituciones.
    """
    r = requests.get(settings.PATH_INSTITUCIONES, headers={"Accept":"application/json"})
    instituciones = r.json()["instituciones"]
    cursos = []
    for institucion in instituciones:
        for curso in institucion["cursos"]:
            cursos.append({
                "id": curso["id"],
                "nombreInstitucion": institucion["nombreInstitucion"],
                "institucionEstudianteId": institucion["id"],
            })
    return cursos

def asignar_estudiantes_a_cursos():
    """
    Crea estudiantes asignados a los cursos embebidos dentro de las instituciones.
    """
    cursos = obtener_cursos_embebidos()

    if not cursos:
        print("No se encontraron cursos en las instituciones.")
        return

    for curso in cursos:
        numero_estudiantes = random.randint(28, 40)
        for _ in range(numero_estudiantes):
            EstudianteFactory(
                nombreEstudiante=Faker('name'),
                codigoEstudiante=Faker('ean13'),
                institucionEstudianteId=curso["institucionEstudianteId"],  # Asignamos el ID único de la institución
                nombreInstitucion=curso["nombreInstitucion"],
                cursoEstudianteId=curso["id"],  # Asignamos el ID único del curso
            )

    print("Estudiantes asignados exitosamente a los cursos.")