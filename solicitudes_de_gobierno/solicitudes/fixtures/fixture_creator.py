from pathlib import Path
import datetime
import json 
import os

data = [
    {
        "model": "solicitudes.tiposdeusuario",
        "pk": 1,
        "fields": {
            "nombre": "Ciudadano",
            "fecha_de_creacion": datetime.date.today().isoformat()
        }
    },
    {
        "model": "solicitudes.tiposdeusuario",
        "pk": 2,
        "fields": {
            "nombre": "Servidor Publico",
            "fecha_de_creacion": datetime.date.today().isoformat()
        }
    },

    {
        "model": "solicitudes.usuario",
        "pk": 1,
        "fields": {
            "nombre": "Abraham",
            "apellido": "Gonzalez",
            "fecha_de_nacimiento": datetime.date(1999, 8, 11).isoformat(),
            "tipo_de_usuario": 1,
            "correo_electronico": "abrahamg@hotmail.com",
            "contrasena": "something",
            "fecha_de_creacion": datetime.date.today().isoformat()
        }
    }
]

fixture_file = os.path.join(Path(__file__).resolve().parent, "0001_fixture.json")

with open(fixture_file, 'w') as json_file:
    json.dump(data, json_file, indent=4)