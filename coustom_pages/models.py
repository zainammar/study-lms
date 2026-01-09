from django.db import models

class PageLink(models.Model):
    page_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)

    content_A = models.TextField(blank=True)
    content_B = models.TextField(blank=True)
    content_C = models.TextField(blank=True)
    content_D = models.TextField(blank=True)
    content_E = models.TextField(blank=True)
    content_F = models.TextField(blank=True)
    content_G = models.TextField(blank=True)
    content_H = models.TextField(blank=True)
    content_I = models.TextField(blank=True)
  

    menu_order = models.PositiveIntegerField(default=0)  # New field for ordering

    def __str__(self):
        return self.page_name
