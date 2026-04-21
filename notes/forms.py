from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Title (optional)',
                'class': 'field',
                'autocomplete': 'off',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your note here…',
                'class': 'field',
                'rows': 8,
            }),
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
        }
        error_messages = {
            'content': {'required': 'Note content cannot be empty.'},
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError('Note content cannot be empty.')
        return content

    def clean_title(self):
        return self.cleaned_data.get('title', '').strip()
