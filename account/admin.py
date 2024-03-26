from django.contrib import admin
from account.models import CustomUser, Profile
from account.models import DeactivateAccount
# from core.models import CardContent

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'role']
    ordering     = ['-id']
    
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id',  'work_place', 'department']
    ordering     = ['-id']
    
class DeactivateAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'confirmation', 'deactivate_status']
    ordering = ['-id']
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(DeactivateAccount, DeactivateAccountAdmin)




















# class CardContentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'title', 'image', 'category', 'created_date']
#     ordering     = ['-id']
    
# admin.site.register(CardContent, CardContentAdmin)