from django.db import models
from django.utils import timezone


class Certificate(models.Model):
    person = models.CharField(max_length=50, null=False, blank=False)
    issue_date = models.DateTimeField(null=False, blank=False, default=timezone.now)
    type = models.CharField(max_length=80, null=False, blank=False)
    token = models.CharField(max_length=100, null=False, blank=False, unique=True)
    link = models.CharField(max_length=200)
    approved_by = models.CharField(max_length=80)
    description = models.TextField(max_length=8192)

    def __str__(self):
        return f"[{self.type}] {self.person}"
