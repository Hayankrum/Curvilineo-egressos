from django import forms
from django_quill.forms import QuillFormField
from .models import Post

class PostForm(forms.ModelForm):
    content = QuillFormField()

    class Meta:
        model = Post
        fields = ['title', 'content']
