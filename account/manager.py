from django.contrib.auth.models import BaseUserManager


# ================================= Custom User Manager =================================
class CustomUserManager(BaseUserManager):
    
    # Create a user
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set")
        if not email:
            raise ValueError("The email field must be set")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create a Superuser
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)