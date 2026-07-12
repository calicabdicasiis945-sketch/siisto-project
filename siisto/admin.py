from django.contrib import admin
from .models import Cunto, Jimicsi, Routine90

# Kani wuxuu qarinayaa animation-ka dhexdiisa Admin-ka isagoo aan waxba ka tirtirin models.py
class JimicsiAdmin(admin.ModelAdmin):
    fields = ['magaca_jimicsiga']  # Kaliya sanduuqa magaca jimicsiga ayaa ka soo muuqan doona admin-ka

admin.site.register(Cunto)
admin.site.register(Jimicsi, JimicsiAdmin)
admin.site.register(Routine90)