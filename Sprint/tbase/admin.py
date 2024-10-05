from django.contrib import admin
from .models import User, Coords, PerevalAdded, PerevalImages


admin.site.register(User)
admin.site.register(Coords)
admin.site.register(PerevalAdded)
admin.site.register(PerevalImages)

