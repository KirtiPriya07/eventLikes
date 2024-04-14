from django import forms
from django.conf import settings

from  .models import Event


MAX_EVENT_LENGTH = settings.MAX_EVENT_LENGTH

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_EVENT_LENGTH:
            raise forms.ValidationError("This Event details are too long")
        return content

