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
from .utils import send_to_rabbitmq


class EstudianteFactory(MongoEngineFactory):
    class Meta:
        model = Estudiante

    nombreEstudiante = Faker('name')
    codigoEstudiante = Faker('ean13')
    
    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """
        Publica un mensaje en RabbitMQ después de crear el estudiante.
        """
        if create:
            message = {
                "type": "estudiante_created",
                "data": {
                    "id": str(instance.id),
                    "nombreEstudiante": instance.nombreEstudiante,
                    "codigoEstudiante": instance.codigoEstudiante,
                    "institucionEstudianteId": str(instance.institucionEstudianteId),
                    "nombreInstitucion": instance.nombreInstitucion,
                    "cursoEstudianteId": str(instance.cursoEstudianteId)
                }
            }
            send_to_rabbitmq(
                exchange='estudiantes',
                routing_key='estudiante.created',
                message=message
            )

def obtener_cursos_embebidos():
    """
    Conecta a la base de datos remota y obtiene los cursos embebidos dentro de las instituciones.
    """
    r = requests.get(settings.PATH_INSTITUCIONES + "/listar-instituciones/", headers={"Accept":"application/json"})
    if r.status_code != 200:
        print("Error al obtener las instituciones.")
        return []
    instituciones = r.json()["instituciones"]
    print("Instituciones obtenidas exitosamente.")
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
        print(f"{numero_estudiantes} estudiantes asignados al curso {curso['id']} de la institución {curso['nombreInstitucion']}.")

    print("Estudiantes asignados exitosamente a los cursos.")