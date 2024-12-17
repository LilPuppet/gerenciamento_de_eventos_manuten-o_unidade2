"""Views Base User"""
from rest_framework import viewsets
from .serializers import UsuarioSerializer
from .models import Usuario


class UsuarioViewSet(viewsets.ModelViewSet):
    """View Base User"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
