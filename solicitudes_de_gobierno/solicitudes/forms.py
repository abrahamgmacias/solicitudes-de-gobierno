from django import forms
from .models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'usuario',
            'accion', 
            'espacio',
            'prioridad',
            'estado',
            'municipio_ciudad',
            'codigo_postal',
            'direccion',
            'informacion_adicional'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control custom-input'