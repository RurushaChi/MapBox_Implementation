from django import forms
from .models import CustomForm


class CustomFormBuilderForm(forms.ModelForm):
    class Meta:
        model = CustomForm
        fields = ["title", "description", "is_active"]
