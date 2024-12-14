from django.contrib import admin

# Register your models here.
from .models import Contact,Chat

# Register the models
admin.site.register(Contact)
admin.site.register(Chat)
