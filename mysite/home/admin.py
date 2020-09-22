from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(forum)
admin.site.register(Discussion)
admin.site.register(Profile)
admin.site.register(options)
admin.site.register(forum_tags)