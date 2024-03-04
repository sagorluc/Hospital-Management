from django import forms
from .models import Profile, CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'frist_name',
            'last_name',
            'email',
            'phone',
            'address',
            'role',
        ]
        labels = {
            'username': 'Username',
            'frist_name': 'Frist Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'address': 'Address',
            'role': 'Role',
            
        }
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_pic', 
            'additional_address', 
            'registration_number', 
            'work_place', 
            'department', 
            'address',
            ]
        labels = {
            'profile_pic' : 'Upload Profile Photo',
            'additional_address': 'Additional Address',
            'registration_number': 'Registration Number',
            'work_place': 'Work Place',
            'department': 'Department',
            'address': 'Address',
        }