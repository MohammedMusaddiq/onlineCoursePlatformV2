from django.contrib import admin
from .models import Content, Course, CourseRegistration


class ContentInline(admin.StackedInline):
    model = Content
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    inlines = [ContentInline]
    list_display = ['teacher', 'title',
                    'created_on', 'updated_on']


admin.site.register(Course, CourseAdmin)


class CourseRegiterationAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'registration_date']


admin.site.register(CourseRegistration, CourseRegiterationAdmin)
