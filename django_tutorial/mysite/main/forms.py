from django import forms

class CreateNewList(forms.Form):
    # list all attributes of form
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)