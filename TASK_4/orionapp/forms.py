# your_app_name/forms.py
from django import forms
from .models import EmployeeDetails, AccessDetails # Import AccessDetails model

class UsernameCSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file',
        help_text='Upload a CSV file containing usernames to match with employees. The first column will be treated as the username column.'
    )

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetails
        fields = ['emp_id', 'name', 'email', 'company', 'status', 'updated_time']
        # Add widgets for better UI control, e.g., for date pickers or text inputs
        widgets = {
            'updated_time': forms.DateInput(attrs={'type': 'date'}),
            'emp_id': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'name': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'email': forms.EmailInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'company': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'status': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

class AccessDetailsForm(forms.ModelForm):
    class Meta:
        model = AccessDetails
        fields = ['user_name', 'app', 'role', 'email', 'status', 'server_name', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'user_name': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'app': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'role': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'email': forms.EmailInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'status': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'server_name': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }
