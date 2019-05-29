from django import forms  
class BlogForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    body = forms.CharField(widget=forms.Textarea, required=False)
    author = forms.CharField(max_length=100, required=False)
    file = forms.FileField(required=False)