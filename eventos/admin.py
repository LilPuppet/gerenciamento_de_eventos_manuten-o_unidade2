from django.contrib import admin # type: ignore
from .models import Local, Evento, Custo

admin.site.register(Local)
admin.site.register(Evento)
admin.site.register(Custo)