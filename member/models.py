from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='avatars/', null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    medical_history = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username']

    groups = models.ManyToManyField(
        Group,
        related_name='userprofile_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='userprofile_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return f'{self.full_name} - {self.date_of_birth.strftime("%Y/%m/%d")}'
