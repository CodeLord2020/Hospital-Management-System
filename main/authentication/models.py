from django.db import models
import uuid


# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class Usermanager(BaseUserManager):
    
    def create_user(self, email, user_name, password, **other_fields):
        
        if not email:
            raise ValueError("Provide a valid email.")
        email = self.normalize_email(email=email)
        user = self.model(email=email, user_name = user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('staff privilege must be assigned to superuser')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser privilege must be assigned to superuser')

        return self.create_user(email, user_name = user_name, password = password,**other_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=50, null=False, blank= False)
    surname = models.CharField(max_length=50, null=False, blank= False)
    first_name = models.CharField(max_length=50, null=False, blank= False)
    last_name = models.CharField(max_length=50, null=True, blank= True)
    otp = models.CharField(max_length=50, null= True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models. BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_medical_staff = models.BooleanField(default=False)
    is_final_authority = models.BooleanField(default=False)

    objects = Usermanager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'surname', 'first_name']
    
    @property
    def get_full_name(self):
        return f"{self.surname.capitalize()} {self.first_name.capitalize()}"
    @property
    def get_user_id(self):
        return str(self.id)

    def __str__(self):
        return self.user_name