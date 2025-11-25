from django.db import models

class Specialty(models.Model):
    """Especialidad médica (ej: Cardiología, Pediatría, etc.)"""
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name