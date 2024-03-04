from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from account.manager import CustomUserManager
from account.constants import CHOICES

# Create your models here
# ================================= Custom User =======================================
class UserPassword(models.Model):
    username     = models.CharField(max_length=150)
    see_password = models.CharField(max_length=8)
    user_id      = models.IntegerField()
    
    
class CustomUser(AbstractBaseUser):   
    username   = models.CharField(max_length=150, null=False, unique=True)
    frist_name = models.CharField(max_length=150, null=True)
    last_name  = models.CharField(max_length=150, null=True)
    email      = models.EmailField(max_length=50, null=False)
    phone      = models.CharField(max_length=14,  null=False)
    address    = models.CharField(max_length=200, null=True)
    role       = models.CharField(max_length=100, choices=CHOICES)
    password   = models.CharField(max_length=8, null=False)
    has_changed_init_pass = models.BooleanField(default=False)
    
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        
    def has_perm(self, perm, obj=None):
        # Check if the user has the specified permission
        return self.is_superuser or self.user_permissions.filter(codename=perm).exists()

    def has_module_perms(self, app_label):
        # Check if the user has permissions for the specified app
        return self.is_superuser or self.user_permissions.filter(content_type__app_label=app_label).exists()

    def __str__(self):
        return self.username
      

# ================================= User Profile ======================================
class Profile(models.Model):
    user                = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='users')
    profile_pic         = models.ImageField(upload_to='photos/', null=True)
    additional_address  = models.CharField(max_length=200, null=True)
    registration_number = models.CharField(max_length= 100, null=False)
    work_place          = models.CharField(max_length=100, null=False)
    department          = models.CharField(max_length=150, null=False)
    address             = models.CharField(max_length=200, null=False)
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        
    def __str__(self) -> str:
        return self.user.username

















# class CardContent(models.Model):
#     user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
#     title        = models.CharField(max_length=200, null=False)
#     image        = models.ImageField(upload_to='photos/')
#     description  = models.TextField()
#     category     = models.CharField(max_length=150, null=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modify_date  = models.DateTimeField(auto_now=True)
    
    
#     class Meta:
#         verbose_name = 'Card Content'
#         verbose_name_plural = 'Card Contents'
        
#     def __str__(self):
#         return self.title