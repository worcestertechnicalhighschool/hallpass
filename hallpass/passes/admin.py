from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
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

class DestinationResource(resources.ModelResource):
    class Meta:
        model = Destination
        fields = ('id','building', 'room', 'category', 'max_people_allowed')
   

class DestinationImportExportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DestinationResource
    list_display = ('id','building', 'room', 'category', 'max_people_allowed')

admin.site.register(Destination, DestinationImportExportAdmin)

class HallPassAdminResource(resources.ModelResource):
    class Meta:
        model = HallPass
        fields = ('id', 'student_id__student_id', 'student_id__first_name', 'student_id__last_name', 'destination__room', 'time_in', 'time_out', 'arrival_time')

from django.utils import timezone
from datetime import timedelta
class HallPassListFilter(admin.SimpleListFilter):
    title = "Weekly Report"
    parameter_name = "week"

    def lookups(self, request, model_admin):
        return [
            ("0", "This Week"),
            ("1", "Last Week"),
            ("2", "2 Weeks ago"),
        ]
    
    def queryset(self, request, queryset):
        # check to see if "week=" param is in url
        if self.value():
            weeks_past = int(self.value())
            today = timezone.now()
            last_monday = today + timedelta(days=-today.weekday(), weeks=-weeks_past)
            return queryset.filter(time_in__gte = last_monday).filter(time_in__lte = last_monday + timedelta(5))

class HallPassImportExportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = HallPassAdminResource
    
    readonly_fields = ('arrival_time',"time_in","time_out",'user')
    list_filter = (HallPassListFilter, 'time_in', 'time_out', "student_id", "destination", "building", "user")
    list_display = ('student_id', 'destination', 'time_in', 'time_out', 'user')

admin.site.register(HallPass, HallPassImportExportAdmin)

from .forms import CategoryForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm

# admin.site.register(Building)
admin.site.register(Profile)
# admin.site.register(Destination)

# default: "Django Administration"
admin.site.site_header = 'HallPass Admin'

# default: "Site administration"
admin.site.index_title = 'Passes Administration'  

# default: "Django site admin"
admin.site.site_title = 'HallPass'    
                 