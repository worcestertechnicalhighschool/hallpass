from django.contrib import admin
from .models import Student, Destination, Log, Building, Profile, Category
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field

admin.site.register(Student)

class LogAdminResource(resources.ModelResource):
    student_id = Field(attribute = "student_id")
    destination = Field(attribute = "destination")
    
    class Meta:
        model = Log
        exclude = ('id',)
        fields = ('student_id', 'destination', 'Time_in', 'Time_out')

class LogsImportExportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = LogAdminResource
    
    readonly_fields = ("Time_in","Time_out")
    list_filter = ('Time_in', 'Time_out', "student_id", "destination")
    list_display = ('student_id', 'destination', 'Time_in', 'Time_out')

admin.site.register(Log, LogsImportExportAdmin)

from .forms import CategoryForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm

admin.site.register(Building)
admin.site.register(Profile)
admin.site.register(Destination)