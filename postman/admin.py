from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( 
    Post,
    ContactGroups,
    ActivityLog,
    ServiceTypes,
    TopUps,
    Credits,
    )

class AppAdmin(admin.ModelAdmin):
    pass