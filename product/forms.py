from department.models import Department
from django import forms


class AddProduct(forms.Form):
    name            = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), required=True)
    amount          = forms.DecimalField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'decimal'}), required=True)
    quantity        = forms.CharField(widget=forms.NumberInput(attrs={'class' : 'form-control'}), required=True)
    manufacturing   = forms.CharField(widget=forms.DateInput(attrs={'class' : 'form-control', 'type':'date'}), required=True)
    expiry          = forms.DateField(widget=forms.DateInput(attrs={'class' : 'form-control', 'type':'date'}), required=True)
    department      = forms.ModelChoiceField(Department.objects.all(), widget=forms.Select(attrs={'class' : 'form-control'}), required=True)

class EditproductForm(forms.Form):
    pro_id          = forms.CharField(widget=forms.HiddenInput(), required=True)
    name            = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), required=True)
    amt             = forms.DecimalField(widget=forms.TextInput(attrs={'class' : 'form-control', 'type':'decimal'}), required=True)
    quantity        = forms.CharField(widget=forms.NumberInput(attrs={'class' : 'form-control'}), required=True)
    manufacturing   = forms.DateField(widget=forms.DateInput(attrs={'class' : 'form-control', 'type':'date'}), required=True)
    expiry          = forms.DateField(widget=forms.DateInput(attrs={'class' : 'form-control', 'type':'date'}), required=True)
    department      = forms.ModelChoiceField(Department.objects.all(), widget=forms.Select(attrs={'class' : 'form-control'}), required=True)