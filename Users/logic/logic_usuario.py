from ..models import Usuario

def get_usuarios():
    queryset = Usuario.objects.all()
    return (queryset)
