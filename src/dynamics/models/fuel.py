from django.db import models as m


class Fuel(m.Model):
    name = m.TextField(unique=True)
    short_name = m.TextField(unique=True)
    color = m.TextField(unique=True)

    class Meta:
        ordering = ["name"]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"

    def __str__(self):
        return f"{self.name} ({self.pk})"
