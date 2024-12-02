from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from estudiantesService.models import Estudiante


@csrf_exempt
def get(request):
        estudiantes = Estudiante.objects.all()
        resultado = []
        for estudiante in estudiantes:
            resultado.append({
                "id": str(estudiante.id),
                "nombreEstudiante": estudiante.nombreEstudiante,
                "codigoEstudiante": estudiante.codigoEstudiante,
                "institucionEstudianteId": str(estudiante.institucionEstudianteId),
                "nombreInstitucion": estudiante.nombreInstitucion,
                "cursoEstudianteId": str(estudiante.cursoEstudianteId),
            })
        return JsonResponse({"estudiantes": resultado})