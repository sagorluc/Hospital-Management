from django import forms
from .models import Profile, CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'frist_name',
            'last_name',
            'username',
            # 'email',
            'phone',
            # 'regis_num',
            # 'role',
        ]
        labels = {
            'username': 'Username',
            'frist_name': 'Frist Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone',
            'regis_num': 'Registration Number',
            'address': 'Address',
            'role': 'Role',
            
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'frist_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your frist name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'regis_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your registration number'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your role'}),
            
        }
        
    # Override the __init__ method to make email and regis_num fields not required
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'].required = False
        # self.fields['regis_num'].required = False
        # self.fields['role'].required = False
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_pic', 
            'department',          
            'work_place',              
            'address',
            'additional_address',
            ]
        labels = {
            'profile_pic' : 'Upload Profile Photo',
            'additional_address': 'Additional Address',
            'registration_number': 'Registration Number',
            'work_place': 'Work Place',
            'department': 'Department',
            'address': 'Address',
        }
        widgets = {
            # 'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload image'}),
            'additional_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Additional address'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration number'}),
            'work_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your work place'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your department'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
                   
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)               
        self.fields['department'].required = False
        self.fields['work_place'].required = False
        self.fields['address'].required = False
        self.fields['additional_address'].required = False