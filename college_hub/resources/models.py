from django.db import models
from django.conf import settings

class Resource(models.Model):
    TYPE = [('notes','Notes'),('PYQ','PYQ'),('book','Book')]
    title = models.CharField(max_length=200)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/')
    type = models.CharField(max_length=10, choices=TYPE)
    downloads = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)
    is_important = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    score = models.IntegerField()
    class Meta: unique_together = ('user', 'resource')

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    reason = models.TextField()

class ResourceRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    description = models.TextField()
    is_fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)