from django import forms
from .models import comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    to = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

class CommentForm(forms.ModelForm) :
    class Meta :
        model = comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }