from django.shortcuts import redirect, render
from account.models import DeactivateAccount
import logging

logger = logging.getLogger(__name__)

def user_is_deactivate_username(username):
    is_deactivate_username = DeactivateAccount.objects.filter(username=username).exists()

    
    if is_deactivate_username:
        logger.warning('This user is deactivated')
        return True
    else:
        return False
    

def user_is_deactivate_email(email):
    is_deactivate_username = DeactivateAccount.objects.filter(email=email).exists()
    
    if is_deactivate_username:
        logger.warning('This user is deactivated')
        return True
    else:
        return False