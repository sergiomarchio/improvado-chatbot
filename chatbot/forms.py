from django import forms
from django.utils.translation import gettext_lazy as _


class ChatForm(forms.Form):
    text_field_attrs = {
        'id': "input-field",
        'class': "input-field",
        'placeholder': _('Type your message here...')
    }

    text_field = forms.CharField(label="",
                                 widget=forms.TextInput(attrs=text_field_attrs))
