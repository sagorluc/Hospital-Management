from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from account.models import DeactivateAccount
import logging

logger = logging.getLogger(__name__)


# =================================== TRACK CHANGES ======================================
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

