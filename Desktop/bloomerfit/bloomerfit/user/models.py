from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    weight=models.DecimalField(max_digits=5, decimal_places=2, default= 1.10)
    height=models.DecimalField(max_digits=5, decimal_places=2, default= 1.10)
    waist=models.DecimalField(max_digits=5, decimal_places=2, default= 1.10)
    hips=models.DecimalField(max_digits=5, decimal_places=2, default= 1.10)
    GENDER=(
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    gender = models.CharField(max_length=6, choices=GENDER, default='Male')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.id}({self.email})"

    
class StatsLogin(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    weight=models.DecimalField(max_digits=5, decimal_places=2, default= 1.10)
    height=models.DecimalField(max_digits=5, decimal_places=2, default= 1.10)
    waist=models.DecimalField(max_digits=5, decimal_places=2, default= 1.10)
    hips=models.DecimalField(max_digits=5, decimal_places=2, default= 1.10)
    time = models.DateTimeField(auto_now=True)

class Contact(models.Model):
    author=models.CharField(max_length=50)
    email=models.EmailField(max_length=64)
    body=models.TextField()

