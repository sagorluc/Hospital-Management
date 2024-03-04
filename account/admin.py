from django.contrib import admin
from account.models import CustomUser, Profile, UserPassword
# from core.models import CardContent

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'role']
    ordering     = ['-id']
    
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'registration_number', 'work_place', 'department']
    ordering     = ['-id']
    
    
class UserPasswordAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'see_password', 'user_id']
    ordering     = ['-id']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserPassword, UserPasswordAdmin)



















# class CardContentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'title', 'image', 'category', 'created_date']
#     ordering     = ['-id']
    
# admin.site.register(CardContent, CardContentAdmin)