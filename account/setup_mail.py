from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from account.models import CustomUser, UserPassword
from account.tokens import account_activation_token

def activateEmail(request, user, to_email):
    
    user_instance = CustomUser.objects.get(pk=user.id)
    user_pass = UserPassword.objects.get(user_id=user_instance.id)
    
    if to_email is None:
        messages.error(request, "Email address is missing.")
        return
            
    mail_subject = "Activate your account"
    html_text = render_to_string("activate_account.html", {
        'user_id'   : user_instance.id,
        'user'      : user_instance.username,
        'frist_name': user_instance.frist_name,
        'last_name' : user_instance.last_name,
        'email'     : to_email,
        'password'  : user_pass.see_password,
        'domain'    : get_current_site(request).domain,
        'uid'       : urlsafe_base64_encode(force_bytes(user_instance.pk)),
        'token'     : account_activation_token.make_token(user),
        'protocol'  : 'https' if request.is_secure() else 'http',
    })
    plain_text = strip_tags(html_text)
    from_email = settings.EMAIL_HOST
    send_mail(mail_subject, plain_text, from_email, [to_email], html_message=html_text)
    mess       = mark_safe(f"Hi <b>{user}</b>, go to your email <b>{to_email}</b>. We have sent a link to activate your account. Note: if it's not found in inbox then check in the spam.")
    messages.success(request, mess)

    # email = EmailMessage(mail_subject, message, to=[to_email])
    # if email.send():
    #     mess = mark_safe(f"Hi <b>{user}</b>, go to your email <b>{to_email}</b>. We have sent a link to activate your account. Note: if it's not found in inbox then check in the spam.")
    #     messages.success(request, mess)
    # else:
    #     mess = mark_safe(f"Problem sending email to <b>{to_email}</b>")
    #     messages.error(request, mess)