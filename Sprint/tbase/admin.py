from django.contrib import admin
from .models import User, Coord, PerevalAdded, PerevalImages, Level

admin.site.register(User)
admin.site.register(Coord)
admin.site.register(PerevalAdded)
admin.site.register(PerevalImages)
admin.site.register(Level)
