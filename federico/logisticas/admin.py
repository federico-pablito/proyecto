from django.contrib import admin
from .models import FormCombination, FormEquipos, SolicitarLogistica

# Register your models here.
admin.site.register(FormEquipos)
admin.site.register(FormCombination)
admin.site.register(SolicitarLogistica)
