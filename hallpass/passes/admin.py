from django.contrib import admin
from .models import Student, Destination, HallPass, Building, Profile, Category
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'student_id', 'building')

class StudentImportExportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StudentResource
    list_display = ('first_name', 'last_name', 'student_id', 'building')

admin.site.register(Student, StudentImportExportAdmin)

class BuildingResource(resources.ModelResource):
    class Meta:
        model = Building
        fields = ('id','building')

class BuildingImportExportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = BuildingResource
    list_display = ('id','building')

admin.site.register(Building, BuildingImportExportAdmin)

class HallPassAdminResource(resources.ModelResource):
    class Meta:
        model = HallPass
        fields = ('id', 'student_id__student_id', 'destination__room', 'Time_in', 'Time_out')


class HallPassImportExportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = HallPassAdminResource
    
    readonly_fields = ("Time_in","Time_out")
    list_filter = ('Time_in', 'Time_out', "student_id", "destination", "building")
    list_display = ('student_id', 'destination', 'Time_in', 'Time_out')

admin.site.register(HallPass, HallPassImportExportAdmin)

from .forms import CategoryForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm

# admin.site.register(Building)
admin.site.register(Profile)
admin.site.register(Destination)
