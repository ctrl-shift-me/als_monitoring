from django import forms
from django.contrib.auth import get_user_model
from .models import KioskOperatorProfile, SuperAgentProfile

class UserRegistrationForm(forms.ModelForm):
  password = forms.CharField(
    label='Password',
    widget=forms.PasswordInput
  )
  
  password2 = forms.CharField(
    label='Repeat password',
    widget=forms.PasswordInput
  )
  
  class Meta:
    model = get_user_model()
    fields = ['email', 'first_name', 'last_name', 'user_type']
    
  def clean_password2(self):
    cd = self.cleaned_data
    if cd['password2'] != cd['password']:
      raise forms.ValidationError("Passwords don't match")
    return cd['password2']
  
  def clean_email(self):
    email = self.cleaned_data['email']
    if get_user_model().objects.filter(email=email).exists():
      raise forms.ValidationError('Email already in use')
    return email
  
  # Todo: handle email-cleaning for edit forms
  
class UserEditForm(forms.ModelForm):
  class Meta:
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email']
    
  
  def clean_email(self):
    email = self.cleaned_data['email']
    if get_user_model().objects.filter(email=email).exclude(id=self.instance.id).exists():
      raise forms.ValidationError('Email already in use')
    return email
  
  
class KioskOperatorProfileForm(forms.ModelForm):
  kiosk_location = forms.CharField(
    label='Kiosk Location',
    widget=forms.TextInput(attrs={'placeholder': 'Enter kiosk location'})
  )
    
  kiosk_id = forms.CharField(
    label='Kiosk ID',
    widget=forms.TextInput(attrs={'placeholder': 'Enter kiosk ID'})
  )
    
  operating_hours = forms.CharField(
    label='Operating Hours',
    widget=forms.TextInput(attrs={'placeholder': 'e.g., 9:00 AM - 5:00 PM'})
  )
    
  phone_number = forms.CharField(
    label='Phone Number',
    widget=forms.TextInput(attrs={'placeholder': '+123456789'})
  )
  
  class Meta:
    model = KioskOperatorProfile
    fields = ['kiosk_location', 'kiosk_id', 'operating_hours', 'phone_number']
    
  def clean_phone_number(self):
    phone = self.cleaned_data['phone_number']
    if not phone.startswith('+'):
      raise forms.ValidationError("Phone number must start with '+'")
    if len(phone) < 10 or len(phone) > 15:
      raise forms.ValidationError("Phone number length is invalid")
    return phone
  
  def clean_kiosk_id(self):
    kiosk_id = self.cleaned_data['kiosk_id']
    if KioskOperatorProfile.objects.filter(kiosk_id=kiosk_id).exists():
      if self.instance and self.instance.kiosk_id != kiosk_id:
        raise forms.ValidationError("This Kiosk ID is already in use")
    return kiosk_id
  

class SuperAgentProfileForm(forms.ModelForm):
  region = forms.CharField(
    label='Region',
    widget=forms.TextInput(attrs={'placeholder': 'Enter region'})
  )
    
  number_of_kiosks_managed = forms.IntegerField(
    label='Number of Kiosks Managed',
    min_value=0,
    widget=forms.NumberInput(attrs={'placeholder': 'Enter number of kiosks'})
  )
    
  phone_number = forms.CharField(
    label='Contact Number',
    widget=forms.TextInput(attrs={'placeholder': '+123456789'})
  )
  
  class Meta:
    model = SuperAgentProfile
    fields = ['region', 'number_of_kiosks_managed', 'phone_number']
    
  def clean_phone_number(self):
    phone = self.cleaned_data['phone_number']
    if not phone.startswith('+'):
      raise forms.ValidationError("Phone number must start with '+'")
    if len(phone) < 10 or len(phone) > 15:
      raise forms.ValidationError("Phone number length is invalid")
    return phone
  
