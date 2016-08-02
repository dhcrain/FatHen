from django import forms
from review_app.models import Status
from django.utils.translation import ugettext_lazy as _

class StatusCreateForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['status_comment', 'status_present', 'status_picture']

        labels = {
            'status_comment': _('Status'),
            'status_present': _('Will you be there?'),
            'status_picture': _('Picture')
        }
        help_texts = {
            'status_present': _('Tell your customers if you will be there.'),
        }

class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)
