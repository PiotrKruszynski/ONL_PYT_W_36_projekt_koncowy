from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


#Status użytkownika
ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('lab_member', 'Personel laboratorium'),
        ('user', 'Klient'),
        ('technician', 'Personel techniczny'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'admin'
    @property
    def is_technician(self):
        return self.role == 'technician'
    @property
    def is_lab_member(self):
        return self.role == 'lab_member'
    @property
    def is_user(self):
        return self.role == 'user'

    def validate_role(self, role):
        if self.role != role:
            raise PermissionDenied(f"Access denied for role: {self.role}")

# co z danymi w przypadku usunięcia użytkownika?