from django.db import models
from .specialty import Specialty

class MedicalProcedure(models.Model):
    """Procedimiento o servicio médico"""
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="procedures")
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    code = models.CharField(max_length=50, unique=True, help_text="Código del procedimiento (ej: CPT, ICD)")
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(default=30, help_text="Duración estimada en minutos")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("specialty", "name")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.code} - {self.name}"