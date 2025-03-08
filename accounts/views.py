from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, KioskOperatorProfileForm, SuperAgentProfileForm

def register(request):
  if request.method == 'POST':
    user_form = UserRegistrationForm(request.POST)
    
    # Select profile form based on user type
    # user_type = request.POST.get('user_type')
    # if user_type == get_user_model().UserType.KIOSK_OPERATOR:
    #   profile_form = KioskOperatorProfileForm(request.POST)
    # elif user_type == get_user_model().UserType.SUPER_AGENT:
    #   profile_form = SuperAgentProfileForm(request.POST)
    # else:
    #   profile_form = None
      
    # print('userform is valid', user_form.is_valid())
    # print('profile form is', profile_form)
    # print('profile form is valid', profile_form.is_valid())
    # Validate both forms
    # if user_form.is_valid() and profile_form and profile_form.is_valid():
    if user_form.is_valid():
      # Create user
      new_user = user_form.save(commit=False)
      new_user.set_password(
        user_form.cleaned_data['password']
      )
      new_user.save()
      
      # Create profile
      # profile = profile_form.save(commit=False)
      # profile.user = new_user
      # profile.save()
      
      messages.success(request, "Account created successfully")
      return render(
        request,
        'accounts/register_done.html',
        {'new_user': new_user}
      )
  else:
    user_form = UserRegistrationForm()
  return render(
    request,
    'accounts/register.html',
    {'user_form': user_form}
  )
  
@login_required
def dashboard(request):
  return render(
    request,
    'accounts/dashboard.html',
    {'section': 'dashboard'}
  )
  
@login_required
def edit_profile(request):
  user = request.user
  
  if request.method == 'POST':
    user_form = UserEditForm(request.POST, instance=user)
    
    # select appropriate form based on user type
    if user.user_type == get_user_model().UserType.KIOSK_OPERATOR:
      profile_form = KioskOperatorProfileForm(
        request.POST,
        instance=getattr(user, 'kioskoperatorprofile', None))
    else:
      profile_form = SuperAgentProfileForm(
        request.POST,
        instance=getattr(user, 'superagentprofile', None))
      
    # validate both forms
    if user_form.is_valid() and profile_form.is_valid():
      # todo: put these in a transaction
      user_form.save()
      
      # save profile
      profile = profile_form.save(commit=False)
      profile.user = user
      profile_form.save()
      
      user.profile_completed = True
      user.save()
      
      messages.success(request, 'Profile updated successfully')
      return redirect('dashboard') # Change this to profile view
  else:
    user_form = UserEditForm(instance=user)
    
    # select appropriate profile form
    if user.user_type == get_user_model().UserType.KIOSK_OPERATOR:
      profile_form = KioskOperatorProfileForm(instance=getattr(user, 'kioskoperatorprofile', None))
    else:
      profile_form = SuperAgentProfileForm(instance=getattr(user, 'superagentprofile', None))
  
  return render(request, 'accounts/edit_profile.html', {
    'user_form': user_form,
    'profile_form': profile_form
  })
  
# redirect user if profile incomplete
# from django.contrib.auth.decorators import user_passes_test

# def incomplete_profile_check(user):
#     return not user.profile_completed

# @user_passes_test(incomplete_profile_check, login_url='edit_profile')
# def dashboard(request):
#     # Your dashboard logic
#     return render(request, 'dashboard.html')