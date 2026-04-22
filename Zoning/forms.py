from django import forms


class AddressZoneCheckForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        label="Home address"
    )