from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile, Department

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'roleSelect'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    roll_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024-CS-101'})
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'roll_number', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'email', 'first_name', 'last_name']:
            if field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if not roll_number or not str(roll_number).strip():
            return None
        return str(roll_number).strip()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role', User.Role.STUDENT)
        user.department = self.cleaned_data.get('department')
        
        roll_num = self.cleaned_data.get('roll_number')
        if roll_num and str(roll_num).strip():
            base_roll = str(roll_num).strip()
            unique_roll = base_roll
            counter = 1
            # Ensure roll_number is completely unique in the database
            while User.objects.filter(roll_number__iexact=unique_roll).exclude(pk=user.pk).exists():
                unique_roll = f"{base_roll}-{counter}"
                counter += 1
            user.roll_number = unique_roll
        else:
            user.roll_number = None

        phone_num = self.cleaned_data.get('phone_number')
        user.phone_number = str(phone_num).strip() if phone_num and str(phone_num).strip() else None
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')

        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Roll Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['bio', 'skills', 'github_url', 'linkedin_url', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, React, MySQL'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://portfolio.dev'}),
        }
