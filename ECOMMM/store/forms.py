from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class register(UserCreationForm):
    email=forms.EmailField()
    class Meta:
          model=User 
          fields=['username','email','password1','password2']
          
    
      
class LoginForm(forms.Form):
        username=forms.CharField(max_length=200)
        password=forms.CharField(max_length=200)
        
        
        
class Search(forms.Form):
     
     query=forms.CharField(max_length=100, required=False, label='Search')
     
    
            