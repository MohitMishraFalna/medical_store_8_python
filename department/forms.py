from django import forms


class DepartmentAddForm(forms.Form):
    # Fields
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)

class DepartmentEditForm(forms.Form):
    # Fields
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    dep_id = forms.CharField(widget=forms.HiddenInput(attrs={'class':'form-control'}), required=True)
    