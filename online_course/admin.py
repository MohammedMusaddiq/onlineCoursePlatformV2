from django.contrib import admin
from .models import Course, CourseRegistration


class CourseAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'title',
                    'description', 'created_on', 'updated_on']


admin.site.register(Course, CourseAdmin)


class CourseRegiterationAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'registration_date']


admin.site.register(CourseRegistration, CourseRegiterationAdmin)
