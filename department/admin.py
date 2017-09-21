from django.contrib import admin
from .models import Department, Cleaner, Plumber, Electrician, Painter, Carpenter
# Register your models here.

admin.site.register(Department)
admin.site.register(Cleaner)
admin.site.register(Plumber)
admin.site.register(Electrician)
admin.site.register(Painter)
admin.site.register(Carpenter)
