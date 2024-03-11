from django.contrib import admin
from .models import FormCombination, FormOne, FormTwo

# Register your models here.
admin.site.register(FormTwo)
admin.site.register(FormOne)
admin.site.register(FormCombination)