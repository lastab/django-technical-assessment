from django.db import models
from django.contrib.auth.models import User


class Csv(models.Model):
    file_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="csvs")

    def __str__(self):
        return self.file_name

class Header(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    csv = models.ForeignKey(Csv, on_delete=models.CASCADE, related_name="headers")
    
    def __str__(self):
        return self.name

class Row(models.Model):
    csv = models.ForeignKey(Csv, on_delete=models.CASCADE, related_name="rows")
    content = models.JSONField(default=list)

    def __str__(self):
        return str(self.id)

