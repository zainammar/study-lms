from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


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
