from django.contrib.auth.models import User
from django import forms
from .models import Staff

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'})     
        }
            
        
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('Password must be greater than 8 charecter')
        return password

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'email', 'user_role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'email'     : forms.TextInput(attrs={'class':'form-control'}),
            'user_role' : forms.Select(attrs={'class':'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('Password must be greater then 8 charecter')
        return password

class ResetPWDForm(forms.ModelForm):
    confirm_pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email' : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'}),
        }        

    # clean_data.get also work with the clean() method
    def clean_confirm_pwd(self):
        password = self.cleaned_data.get('password')
        confirm_pwd = self.cleaned_data.get('confirm_pwd')

        if password != confirm_pwd:
            raise forms.ValidationError('Password Din\'t matche with Confirm password.')
        
        return confirm_pwd

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError('Password must be greater than 8 characters.')
        return password

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'dob', 'gender', 'mobile', 'profile_img','pincode', 'city', 'dist', 'state', 'country', 'about_user']

        widgets = {
            'first_name'     : forms.TextInput(attrs={'class':'form-control'}), 
            'last_name'      : forms.TextInput(attrs={'class':'form-control'}), 
            'dob'            : forms.DateInput(attrs={'class':'form-control', 'type':'date'}, format='%d/%m/%Y'), 
            'gender'         : forms.Select(attrs={'class':'form-control'}), 
            'mobile'         : forms.NumberInput(attrs={'class':'form-control'}), 
            'profile_img'    : forms.FileInput(attrs={'class':'form-control'}),
            'pincode'        : forms.NumberInput(attrs={'class':'form-control'}), 
            'city'           : forms.Select(attrs={'class':'form-control', 'readonly':'readonly'}), 
            'dist'           : forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}), 
            'state'          : forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}), 
            'country'        : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}), 
            'about_user'     : forms.Textarea(attrs={'class':'form-control'})
        }
