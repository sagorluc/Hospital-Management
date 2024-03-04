from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from account.models import CustomUser, Profile, UserPassword
from account.form import ProfileForm, CustomUserForm
from account.setup_mail import activateEmail
from account.tokens import account_activation_token

# Create your views here.

# =============================== USER ACTIVATION ACCOUNT ===============================
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, "Thank you for your email confirmation. You have done your registration successfully. Now you are good to go")
        return redirect('login')
    else:
        messages.error(request, "Activation link invalid!")
        
    return redirect('login')   

# ============================ REGISTRATION OF NORMAL USER =============================
@login_required
def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        frist_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        role = request.POST.get('role')
        password = request.POST.get('password')
        
        if request.user.is_superuser:
            create_user = CustomUser.objects.create(
                username=username, 
                frist_name=frist_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                role=role,
            )
            create_user.set_password(password)
            create_user.is_active = False
            create_user.save()
            without_hash_pass = UserPassword.objects.create(
                username=username, 
                see_password=password, 
                user_id=create_user.id,
                )
            without_hash_pass.save()
            activateEmail(request, create_user, email)
            messages.success(request, 'Registration successful. We have sent credentials via email')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration is not possible without superuser privileges')
            return redirect('register')
         
    template = 'registration.html'
    return render(request, template)

# ===================================== USER LOGIN ======================================
def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user exists
        # is_exists = CustomUser.objects.filter(username=username).first()
        # if not is_exists:
        #     messages.error(request, 'User does not exist')
        #     return redirect('login')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        # Check authentication
        if user is not None:
            login(request, user)
            messages.success(request, 'User logged in successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    template = 'login.html'
    return render(request, template)


# ==================================== USER LOGOUT ======================================
@login_required
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'User logout successfully')
        return redirect('login')

    return render(request, 'login.html')
        

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
    
    template = 'dashboard.html'
    return render(request, template, context)


# ================================ USER RESET PASSWORD =================================
@login_required
def reset_user_init_password(request, id=None):
    user_instance = CustomUser.objects.get(pk=id)
    
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confrim_password = request.POST.get('confirm_password')
        
        if not user_instance.check_password(old_password):
            messages.error(request, "Old password does not match")
            return redirect("reset_password", id=user_instance.id)
        
        if new_password != confrim_password:
            messages.error(request, "New password and confrim password does not match")
            return redirect("reset_password", id=user_instance.id)
        
        if request.user.is_authenticated:
            user_instance.set_password(new_password)
            user_instance.has_changed_init_pass = True
            user_instance.save()
            logout(request)
            messages.success(request, "New password set successfully, securely logout.")
            return redirect('login')
    
    return render(request, "reset_password.html", {"user_instance": user_instance})
        
        
# =================================== USER PROFILE ======================================
@login_required
def user_profile(request):
    try:
        user_instance    = CustomUser.objects.get(pk=request.user.id)
        profile_instance = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile_instance = None

    if request.method == 'POST':
        form  = CustomUserForm(request.POST, instance=user_instance)
        form1 = ProfileForm(request.POST, request.FILES, instance=profile_instance)

        if form.is_valid() and form1.is_valid():           
            user_instance = form.save(commit=False)
            user_instance.save()
            
            # previus_user_data = CustomUser.objects.get(pk=user_instance.pk)
            # previus_profile_data = Profile.objects.filter(user=user_instance).first()
            
            # is_changes_user_data = track_changes_user(previus_user_data, user_instance)
            # is_changes_profile_data = track_changes_profile(previus_profile_data, profile_instance)
            
            # if not is_changes_user_data and not is_changes_profile_data:
            #     messages.info(request, "No changes detected.")
            #     return redirect('dashboard')
                       
            if profile_instance is None:
                profile_instance = form1.save(commit=False)
                profile_instance.user = user_instance
            else:
                profile_instance.profile_pic = form1.cleaned_data['profile_pic']
                profile_instance.additional_address = form1.cleaned_data['additional_address']
                profile_instance.registration_number = form1.cleaned_data['registration_number']
                profile_instance.work_place = form1.cleaned_data['work_place']
                profile_instance.department = form1.cleaned_data['department']
                profile_instance.address = form1.cleaned_data['address']
            profile_instance.save()

            messages.success(request, "User profile updated successfully.!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Form')
    else:
        form  = CustomUserForm(instance=user_instance)
        form1 = ProfileForm(instance=profile_instance)

    template = 'profile.html'
    context = {
        'form': form,
        'form1': form1,
    }
   
    return render(request, template, context)



def track_changes_user(previous_data, updated_data):
    changes = {}
    # Compare each field of the event model
    for field in [
            'username',
            'frist_name',
            'last_name',
            'email',
            'phone',
            'address',
            'role',

        ]:
        previous_value = getattr(previous_data, field)
        updated_value = getattr(updated_data, field)
        if previous_value != updated_value:
            changes[field] = {
                'previous_value': previous_value,
                'updated_value': updated_value
            }
    return changes

def track_changes_profile(previous_data, updated_data):
    changes = {}
    # Compare each field of the event model
    for field in [
            'profile_pic', 
            'additional_address', 
            'registration_number', 
            'work_place', 
            'department', 
            'address',
        ]:
        previous_value = getattr(previous_data, field)
        updated_value = getattr(updated_data, field)
        if previous_value != updated_value:
            changes[field] = {
                'previous_value': previous_value,
                'updated_value': updated_value
            }
    return changes









# def user_profile(request):
#     user_instance = CustomUser.objects.get(pk=request.user.id)
#     profile_instance = Profile.objects.get(user=request.user)
    
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST, request.FILES, instance=user_instance)
#         form1 = ProfileForm(request.POST, request.FILES, instance=profile_instance)
#         if form.is_valid() and form1.is_valid():
#             username = form.cleaned_data['username']
#             frist_name = form.cleaned_data['frist_name']
#             last_name = form.cleaned_data['last_name']
#             email = form.cleaned_data['email']
#             phone = form.cleaned_data['phone']
#             address = form.cleaned_data['address']
#             role = form.cleaned_data['role']
#             image = form1.cleaned_data['profile_pic']
#             add_address = form1.cleaned_data['additional_address']
#             regis_number = form1.cleaned_data['registration_number']
#             work_place = form1.cleaned_data['work_place']
#             department = form1.cleaned_data['department']
#             address1 = form1.cleaned_data['address']
            
#             is_user_exists = CustomUser.objects.filter(username=user_instance.username).first()
#             is_profile_exist = Profile.objects.filter(user=request.user).first()
            
#             if is_user_exists and is_profile_exist:
#                 is_user_exists.username = username
#                 is_user_exists.frist_name = frist_name
#                 is_user_exists.last_name = last_name
#                 is_user_exists.email = email
#                 is_user_exists.phone = phone
#                 is_user_exists.address = address
#                 is_user_exists.role = role
#                 is_profile_exist.profile_pic = image
#                 is_profile_exist.additional_address = add_address
#                 is_profile_exist.registration_number = regis_number
#                 is_profile_exist.department = department
#                 is_profile_exist.work_place = work_place
#                 is_profile_exist.address = address1
#                 is_user_exists.save()
#                 is_profile_exist.save()
#                 messages.success(request, "User profile updated successfully.!!")
#                 return redirect('dashboard')
#             else:
#                 create_profile = Profile.objects.create(
#                     profile_pic = image,
#                     additional_address = add_address,
#                     registration_number = regis_number,
#                     work_place = work_place,
#                     department = department,
#                     address = address1
#                 )
#                 create_profile.save()
#                 messages.success(request, 'User profile updated successfully.!!')
#                 return redirect('dashboard')
#         else:
#             messages.error(request, 'Invalid Form')
#             return redirect('profile')
#     else:
#         form = CustomUserForm(instance=user_instance)
#         form1 = ProfileForm(instance=profile_instance)
        
#     template = 'profile.html'
#     context = {
#         'form': form,
#         'form1': form1,
#     }
   
#     return render(request, template, context)




# @login_required
# def profile(request):
#     user = request.user
#     # user_instance = CustomUser.objects.get(pk=user.id)
    
#     if request.method == "POST":
#         # Retrieve form data
#         image = request.FILES.get('image')
#         addi_address = request.POST.get('add_address')
#         regis_number = request.POST.get('regis_number')
#         work_place = request.POST.get('work_place')
#         department = request.POST.get('department')
#         address = request.POST.get('address')

#         # Check if the user already has a profile
#         profile = Profile.objects.filter(user=request.user).first()

#         if profile:
#             # Update existing profile
#             profile.profile_pic = image
#             profile.additional_address = addi_address
#             profile.registration_number = regis_number
#             profile.work_place = work_place
#             profile.department = department
#             profile.address = address
#             profile.save()
#             messages.success(request, 'Profile data updated successfully.')
#             return redirect('dashboard')
#         else:
#             # Create new profile
#             create_profile = Profile.objects.create(
#                 user=user,
#                 profile_pic=image,
#                 additional_address=addi_address,
#                 registration_number=regis_number,
#                 work_place=work_place,
#                 department=department,
#                 address=address,
#             )
#             messages.success(request, 'Profile data saved successfully.')
#             create_profile.save()
#             return redirect('dashboard')
#     else:
#         messages.error(request, 'Invalid request')
        
#     template = 'profile.html'
#     return render(request, template)


# # ================================= USER PROFILE UPDATE =================================
# @login_required
# def update_profile(request):
#     user = request.user
#     # profile_instance = Profile.objects.get(user=user)
#     try:
#         profile_instance = Profile.objects.get(user=user)
#     except Profile.DoesNotExist:
#         profile_instance = None
    
#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile data update successfully.!!")
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Form is not valid.!!")
#             return redirect('update_profile')
#     else:
#         form = ProfileForm(instance=profile_instance)
        
#     template = 'profile_update.html'
#     context = {
#         'form' : form,
#     }
#     return render(request, template, context)




# @login_required
# def update_profile(request):
#     # user = request.user
#     # user_profile_instance = Profile.objects.get(user=user)   
#     try:
#         user_profile_instance = Profile.objects.get(user=request.user)
#     except Profile.DoesNotExist:
#         user_profile_instance = Profile.objects.create(user=request.user)
    
#     if request.method == "POST":
#         image        = request.POST.get('image')
#         addi_address = request.POST.get('add_address')   
#         regis_number = request.POST.get('regis_number')   
#         work_place   = request.POST.get('work_place')   
#         department   = request.POST.get('department')   
#         address      = request.POST.get('address')
        
#         # Update the profile instance with new data
#         user_profile_instance.profile_pic         = image
#         user_profile_instance.additional_address  = addi_address
#         user_profile_instance.registration_number = regis_number
#         user_profile_instance.work_place          = work_place
#         user_profile_instance.department          = department
#         user_profile_instance.address             = address 
        
#         user_profile_instance.save()
#         messages.success(request, "Profile data update successfully.!!")
#         return redirect('dashboard')
#     else:
#         messages.error(request, "Invalid update")
    
#     template = 'profile_update.html'
#     context = {
#         'profile_instance' : user_profile_instance,
#     }
#     return render(request, template, context)