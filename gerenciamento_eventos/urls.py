from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from eventos.views import LocalViewSet, EventoViewSet, CustoViewSet
from usuarios.views import UsuarioViewSet

router = DefaultRouter()
router.register(r'locais', LocalViewSet, basename='locais')
router.register(r'eventos', EventoViewSet, basename='eventos')
router.register(r'custos', CustoViewSet, basename='custos')
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/token-auth/", views.obtain_auth_token),

    path('api/', include(router.urls))
]
    