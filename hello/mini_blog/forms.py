from django import forms
from .models import BlogPost
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content' , 'domain' , 'subject']

