from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class LiveClass(models.Model):
    course = models.ForeignKey(
        'Course',   # ✅ STRING reference (important)
        on_delete=models.CASCADE,
        related_name='live_classes'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    meeting_link = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"




class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(
        'Course',
        related_name='chapters',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('course', 'slug')
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Page(models.Model):
    chapter = models.ForeignKey(
        'Chapter',
        related_name='pages',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('chapter', 'slug')
        ordering = ['order']

    def __str__(self):
        return self.title


@receiver(post_delete, sender=Page)
def delete_files(sender, instance, **kwargs):
    if instance.video and instance.video.name:
        instance.video.delete(save=False)
    if instance.pdf and instance.pdf.name:
        instance.pdf.delete(save=False)


class Enrollment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'course')

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.enrolled_at + timedelta(days=365)

        if timezone.now() >= self.expires_at:
            self.is_active = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} → {self.course.title}"



class Assignment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='assignments',
        blank=True,
        null=True
    )
    title = models.CharField(max_length=200)
    question = models.TextField()
    due_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignment_submissions'
    )
    answer_text = models.TextField(blank=True)
    answer_file = models.FileField(upload_to='assignment_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)
    marks = models.PositiveIntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"