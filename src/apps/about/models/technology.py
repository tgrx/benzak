from django.db import models


class Technology(models.Model):
    name = models.TextField(unique=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "technologies"
        ordering = ["name"]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"

    def __str__(self):
        return f"{self.name} ({self.pk})"
