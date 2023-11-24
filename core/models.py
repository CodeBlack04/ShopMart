from django.db import models

# Create your models here.
class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.full_name}--{self.subject}--{self.message}'
