from django.contrib import admin
from .models import User, Coord, PerevalAdded, PerevalImages


admin.site.register(User)
admin.site.register(Coord)
admin.site.register(PerevalAdded)
admin.site.register(PerevalImages)

