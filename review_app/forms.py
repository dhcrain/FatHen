from django import forms
from review_app.models import Status


class StatusCreateForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['status_comment', 'status_present', 'status_picture']
