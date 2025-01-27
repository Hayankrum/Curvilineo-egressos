from django.db import models
from django_quill.fields import QuillField

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = QuillField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
