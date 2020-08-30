from django.contrib import admin
from . import models
from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

admin.site.register(models.User)
admin.site.register(models.Avatar)
