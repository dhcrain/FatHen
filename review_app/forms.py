from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from review_app.models import Status


class StatusCreateForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["status_comment", "status_present", "status_picture"]

        labels = {
            "status_comment": _("Status"),
            "status_present": _("Will you be there?"),
            "status_picture": _("Picture"),
        }
        help_texts = {
            "status_present": _("Tell your customers if you will be there."),
        }


class ContactForm(forms.Form):
    required_css_class = "required"
    captcha = ReCaptchaField()
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)


# https://djangosnippets.org/snippets/3043/
class UserCreationEmailForm(UserCreationForm):
    required_css_class = "required"
    captcha = ReCaptchaField()
    # we are using email as username so override label and validators
    username = forms.CharField(
        label="Email:",
        max_length=30,
        required=True,
        validators=[validate_email],
        help_text=
        _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
          ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
