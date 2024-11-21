from django.db import models
from django.db.models import F, ExpressionWrapper
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
import datetime

current_date = datetime.date.today()

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided an email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self.db)
        
        return user
    
    def create_user(self, email=None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, default='', blank='True')
    name = models.CharField(max_length=255, blank=True, default='')
    surname = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    profile_img = models.ImageField(default = 'user.jpg')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    @property
    def imageURL(self):
        try:
            url = self.profile_img.url
        except:
            url=''
        return url
        
class Egg(models.Model):
    quantity = models.IntegerField(blank=True, null=True, default=0)
    date = models.DateField(auto_now_add=True)
    
    def get_days_difference(self):
        """Calculates the difference between start_date and end_date in days."""
        if current_date and self.date:
            return (current_date - self.date).days
        else:
            return None  # Handle missing dates (optional)
    
    def __str__(self):
        return str(self.date)
    
class FeedingTimeTable(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField()
    description = models.CharField(max_length=500, blank = True, null = True)
    
    def __str__(self):
        return self.description
    
class ChicksManagement(models.Model):
    batch = models.CharField(max_length=255, unique = True)
    number_of_chicks = models.IntegerField(default=0)
    date = models.DateField()
    
    
    def get_days_difference(self):
        """Calculates the difference between start_date and end_date in days."""
        if current_date and self.date:
            return (current_date - self.date).days
        else:
            return None  # Handle missing dates (optional)
    
    def __str__(self):
        return self.batch