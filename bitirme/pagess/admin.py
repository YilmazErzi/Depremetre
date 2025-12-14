from django.contrib import admin
from .models import Person, BuildingAssessment 


@admin.register(Person)
class teamMember(admin.ModelAdmin):
    list_display = ("first_name","last_name","Department")
    list_display_links = ("first_name","last_name")
    list_filter = ("Department",)


@admin.register(BuildingAssessment)
class BuildingAssessmentAdmin(admin.ModelAdmin):
    list_display = ("building_name", "calculate_total_score", "created_at")
    list_filter = ("created_at",)
    search_fields = ("building_name",)