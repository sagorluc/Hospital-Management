from django.shortcuts import render, redirect
from django.http import HttpResponse
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
from account.models import DeactivateAccount
from account.sub_function import user_is_deactivate_email, user_is_deactivate_username

# Create your views here.

def home(request):
    template = "content/index.html"
    return render(request, template)

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
        username     = request.POST.get('username')
        frist_name   = request.POST.get('frist_name')
        last_name    = request.POST.get('last_name')
        email        = request.POST.get('email')
        phone        = request.POST.get('phone')
        regis_num    = request.POST.get('registration_number')
        role         = request.POST.get('role')
        password     = request.POST.get('password')
        confirm_pass = request.POST.get('repeat_password')
        
        # Check if the email already been used in deactivate account 
        is_deactivated_account_email = user_is_deactivate_email(email)
        if is_deactivated_account_email:
            messages.error(request, 'This email is already been used which account is been deleted. try with another email')
            return redirect('register')
        
        if password != confirm_pass:
            messages.error(request, 'Password does not match')
            return redirect('register')
        
        if request.user.is_superuser:
            create_user = CustomUser.objects.create(
                username=username, 
                frist_name=frist_name,
                last_name=last_name,
                email=email,
                phone=phone,
                show_pass=password,
                regis_num=regis_num,
                role=role,
            )
            create_user.set_password(password)
            create_user.is_active = False
            create_user.save()
            activateEmail(request, create_user, email)
            messages.success(request, 'Registration successful. We have sent credentials via email')
            return redirect('login')
        else:
            messages.error(request, 'Registration is not possible without superuser privileges')
            return redirect('register')
         
    template = 'login-register/signup.html'
    context = {'choices': CHOICES}
    return render(request, template, context)

# ===================================== USER LOGIN ======================================
def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        is_deactivate = user_is_deactivate_username(username)
        
        if is_deactivate:
            messages.error(request, 'User account with this username/email already deacivated')
            return redirect('login')
        
        # Check authentication
        if user is not None:
            login(request, user)
            messages.success(request, 'User logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    template = 'login-register/login.html'
    return render(request, template)


# ==================================== USER LOGOUT ======================================
@login_required
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'User logout successfully')
        return redirect('login')

    return render(request, 'login.html')
        

# ==================================== DELETE USER ======================================
@login_required
def deactivate_account(request):
    user = request.user
    
    try:
        user_instance = CustomUser.objects.get(pk=user.id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('login')
    
    if request.method == 'POST':
        input_user_email = request.POST.get('email')
        current_user_email = user_instance.email
        
        if current_user_email == input_user_email:
            user_instance.save()
                   
            DeactivateAccount.objects.create(
                user=user_instance,
                username=user_instance.username,
                email=user_instance.email,
                confirmation='Done',
                deactivate_status=True
            )
            user_instance.delete()
            
            messages.success(request, 'Account deleted successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Email does not match. Please retype again.')
            return redirect('deactivate_account')
    
    return render(request, 'deactivate_account.html')
            

        
        
        