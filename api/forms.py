# forms.py
from django import forms
from .models import FeedingTimeTable, User, ChicksManagement

class FeedingTimeTableForm(forms.ModelForm):
    class Meta:
        model = FeedingTimeTable
        fields = ['date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'phone', 'profile_img']  # Include the fields you want to update
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            }
from django import forms
from .models import ChicksManagement

class ChicksManagementForm(forms.ModelForm):
    class Meta:
        model = ChicksManagement
        fields = ['batch', 'number_of_chicks', 'date']
        widgets = {
            'batch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter batch name'}),
            'number_of_chicks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of chicks'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ChicksManagementForm(forms.ModelForm):
    class Meta:
        model = ChicksManagement
        fields = ['batch', 'number_of_chicks', 'date']
        widgets = {
            'batch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter batch name'}),
            'number_of_chicks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of chicks'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }