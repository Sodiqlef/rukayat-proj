from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    shared_with = models.ManyToManyField(User, related_name='shared_notes', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']