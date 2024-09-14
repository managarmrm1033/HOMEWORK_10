from django.forms import ModelForm, CharField, TextInput
from .models import Tag, Note
from .models import Author
from django import forms

class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']

class NoteForm(ModelForm):
    name = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=150, required=True, widget=TextInput())
    author = forms.ModelChoiceField(queryset=Author.objects.none(), required=True)

    class Meta:
        model = Note
        fields = ['name', 'description', 'author']
        exclude = ['tags']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['author'].queryset = Author.objects.filter(user=user)

class AuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ['name']