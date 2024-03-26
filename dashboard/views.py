from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from account.models import CustomUser, Profile
from account.form import ProfileForm, CustomUserForm
from account.setup_mail import activateEmail
from account.tokens import account_activation_token
from account.constants import CHOICES

# Create your views here.
def create_news(request):
    template = 'dashboard/news-form.html'
    return render(request, template)


# ================================== USER DASHBOARD =====================================
@login_required
def dashboard(request):
    user = request.user
    user_id = user.id
    user_instance = CustomUser.objects.get(pk=user_id)
    has_changed_init_pass = user_instance.has_changed_init_pass
    disable_content = not has_changed_init_pass
    
    context = {
        'user_instance': user_instance,
        'disable_content': disable_content
    }
    
    template = 'dashboard/videos.html'
    return render(request, template, context)


# ================================ USER RESET PASSWORD =================================
@login_required
def show_user_profile_data(request):
    try:
        user_instance = CustomUser.objects.get(pk=request.user.id)
    except CustomUser.DoesNotExist:
        user_instance = None
    
    try:
        profile_instance = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile_instance = None
        
    print(user_instance.frist_name, 'line 49')
    print(profile_instance, 'line 50')
    
    context = {
        'user' : user_instance,
        'profile' : profile_instance
    }
    template = 'dashboard/profile.html'
    return render(request, template, context)
        
        
# =================================== USER PROFILE ======================================

@login_required
def update_user_profile(request):
    try:
        user_instance = CustomUser.objects.get(pk=request.user.id)
    except CustomUser.DoesNotExist:
        user_instance = None
        
    try:
        profile_instance = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile_instance = None

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user_instance)
        form1 = ProfileForm(request.POST, request.FILES, instance=profile_instance)

        # Check if each form is valid separately
        if form.is_valid() and form1.is_valid():
            image      = form1.cleaned_data['profile_pic']
            address1   = form1.cleaned_data['address']
            address2   = form1.cleaned_data['additional_address']
            work       = form1.cleaned_data['work_place']
            department = form1.cleaned_data['department']
            
            user_instance = form.save(commit=False)
            user_instance.save()
            profile_instance = form1.save(commit=False)
            profile_instance.user = request.user  # Set the user field
            profile_instance.save()

            messages.success(request, "User profile updated successfully.")
            return redirect('show_profile')
        else:
            messages.error(request, 'Invalid Form')
            return redirect('update_profile')

    else:
        form = CustomUserForm(instance=user_instance)
        form1 = ProfileForm(instance=profile_instance)

    template = 'dashboard/profile_update.html'
    context = {
        'form': form,
        'form1': form1,
        # 'choices': CHOICES
    }
   
    return render(request, template, context)



# ================================ USER RESET PASSWORD =================================
@login_required
def reset_user_init_password(request):
    user = request.user
    user_instance = CustomUser.objects.get(pk=user.id)
    
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confrim_password = request.POST.get('repeat_password')
        
        if not user_instance.check_password(old_password):
            messages.error(request, "Old password does not match")
            return redirect("reset_password")
        
        if new_password != confrim_password:
            messages.error(request, "New password and confrim password does not match")
            return redirect("reset_password")
        
        if request.user.is_authenticated:
            user_instance.set_password(new_password)
            user_instance.has_changed_init_pass = True
            user_instance.save()
            logout(request)
            messages.success(request, "New password set successfully, securely logout.")
            return redirect('login')
    
    return render(request, "dashboard/change_password.html", {"user_instance": user_instance})