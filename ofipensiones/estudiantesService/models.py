from mongoengine import Document, fields
class Estudiante(Document):
    nombreEstudiante =  fields.StringField(max_length=100)
    codigoEstudiante = fields.StringField(max_length=50)

    # Relaciones con otras BD
    institucionEstudianteId = fields.ObjectIdField(editable=False)
    nombreInstitucion = fields.StringField(max_length=100)
    cursoEstudianteId = fields.ObjectIdField()

    def __str__(self):
        return self.nombreEstudiante