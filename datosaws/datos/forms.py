from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Expense, Category, Income
from django.forms import ModelForm


class ExpenseForm(ModelForm):
    category_name = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            widget=forms.Select(attrs={'class': 'form-select'})
        )

    class Meta:
        model = Expense
        exclude = ['user']  # Exclude user field, as it is set in the view
        widgets = {
            'category_name': forms.Select(attrs={'class': 'form-select'})  # Add Bootstrap form-select class for consistency
        }

class IncomeForm(ModelForm):
    category_name = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Income
        exclude = ['user']  # Exclude user field, as it is set in the view
        widgets = {
            'category_name': forms.Select(attrs={'class': 'form-select'})
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))



    #     widgets = {
    #         'category_name': forms.Select(attrs={'class': 'form-select'})
    #     }

    # # Override the category_name field to use ChoiceField
    # category_name = forms.ModelChoiceField(queryset=Category.objects.all())

    # def __init__(self, *args, **kwargs):
    #     super(ExpenseForm, self).__init__(*args, **kwargs)
    #     # Populate choices for the category_name field
    #     unique_categories = Expense.objects.values_list('category_name__category_name', flat=True).distinct()
    #     self.fields['category_name'].choices = [(category, category) for category in unique_categories]