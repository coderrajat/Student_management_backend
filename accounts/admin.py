from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin


#admin.site.register(Account, AccountAdmin)
admin.site.register(models.User)
admin.site.register(models.User_token)