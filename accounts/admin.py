from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Investor)
admin.site.register(Investment)
admin.site.register(Update)