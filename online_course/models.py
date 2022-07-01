from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    teacher = models.ForeignKey(
        User, related_name='teacher', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = ('Courses')
        ordering = ('-created_on', '-updated_on')

    def __str__(self):
        return str(self.title)


class Content(models.Model):
    course = models.ForeignKey(
        Course, related_name='courses', on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'contents'

    def __str__(self):
        return str(self.topic)


class CourseRegistration(models.Model):
    student = models.ForeignKey(
        User, related_name='student', on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, related_name='course', on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = ('Course Registrations')
        ordering = ('-student',)

    def __str__(self):
        return str(self.student) + str(self.course)
