from django.contrib import admin
from .models import Dorm, Vouch, School

# Register your models here.
class DormAdmin(admin.ModelAdmin):
    list_display = ("name", "dorm_location", "display_school",)
    list_filter = ("dorm_location",)

class VouchAdmin(admin.ModelAdmin):
    list_display = ("__str__", "submitted_by_name", "dorm", "rating", "review",)
    list_filter = ("rating", "dorm")

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "school_location",)
    list_filter = ("school_location",)

admin.site.register(Dorm, DormAdmin)
admin.site.register(Vouch, VouchAdmin)
admin.site.register(School, SchoolAdmin)