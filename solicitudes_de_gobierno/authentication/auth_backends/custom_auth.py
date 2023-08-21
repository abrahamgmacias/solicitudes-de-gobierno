from django.contrib.auth.backends import ModelBackend

class CustomAuthenticate(ModelBackend):
    def authenticate(self, request, correo_electronico=None, contrasena=None, **kwargs):
        from usuarios.models import Usuario
        try:
            usuario = Usuario.objects.get(correo_electronico=correo_electronico, activo=True)

        except Usuario.DoesNotExist:
            return None

        if usuario.checarContrasena(contrasena):
            return usuario

        return None