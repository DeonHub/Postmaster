from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( 
    # RecievedDutyReports,
    # ExtraWorkReport, 
    # AssignedDutyActivities, 
    Nameken
    )

class AppAdmin(admin.ModelAdmin):
    pass