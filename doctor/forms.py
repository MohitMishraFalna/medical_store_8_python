from django import forms
from .models import Doctor


class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'email', 'mobile', 'department']
        widgets = {
            'name'       : forms.TextInput(attrs={'class': 'form-control'}),
            'email'      : forms.TextInput(attrs={'class': 'form-control'}),
            'mobile'     : forms.NumberInput(attrs={'class': 'form-control'}),
            'department' : forms.Select(attrs={'class': 'form-control'}),
        }

class EditDoctorForm(forms.ModelForm):
    id = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}), required=True)
    class Meta:
        model = Doctor
        fields = ['name', 'email', 'mobile', 'department']
        widgets = {
            'name'       : forms.TextInput(attrs={'class': 'form-control'}),
            'email'      : forms.TextInput(attrs={'class': 'form-control'}),
            'mobile'     : forms.NumberInput(attrs={'class': 'form-control'}),
            'department' : forms.Select(attrs={'class': 'form-control'}),
        }
