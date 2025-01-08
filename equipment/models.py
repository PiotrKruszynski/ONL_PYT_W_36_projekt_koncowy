from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class CalibrationProvider(models.Model):
    """ Model reprezentujący jednostkę wzorcującą.
    W przyszłości może zostać rozszerzony o pola z zakresem badań i ceną"""
    calib_prov_name = models.CharField(max_length=150)  # Nazwa dostawcy
    contact_email = models.EmailField(blank=True, null=True)  # Opcjonalny e-mail
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Opcjonalny telefon
    address = models.TextField(blank=True, null=True)  # Opcjonalny adres

    def __str__(self):
        return self.calib_prov_name

EQUIPMENT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('damaged', 'Damaged'),
        ('uncalibrated', 'Uncalibrated'),
        ('maintenance', 'Maintenance'),
        ('b2b', 'Business-to-Business (B2B Use Only)'),
    ]

class Equipment(models.Model):
    """Model reprezentujący wyposażenie lab."""
    equipment_name = models.CharField(max_length=100)  # Nazwa aparatury
    description = models.TextField(blank=True, null=True)  # Opcjonalny opis
    status = models.CharField(
        max_length=20,
        choices=EQUIPMENT_STATUS_CHOICES,
        default='available'
    )  # Status aparatury
    purchase_date = models.DateField(blank=True, null=True)  # Data zakupu aparatury
    last_calibration_date = models.DateTimeField(blank=True, null=True)  # Data ostatniego wzorcowania
    next_calibration_date = models.DateTimeField(blank=True, null=True)  # Data kolejnego wzorcowania
    last_maintenance_date = models.DateTimeField(blank=True, null=True)  # Data ostatniej konserwacji
    assigned_to = models.ForeignKey(
        'Profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_equipment'
    )  # Kto jest przypisany do aparatury
    calibration_provider = models.ForeignKey(
        CalibrationProvider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calibrated_equipment'
    )  # Jednostka wzorcująca
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.equipment_name} ({self.get_status_display()})"

    def is_calibration_due(self):
        """Sprawdza czy wzorcowanie jest wymagane."""
        if self.next_calibration_date:
            return self.next_calibration_date <= timezone.now()
        return False

    def days_until_next_calibration(self):
        """Zwraca liczbę dni do następnego wzorcowania."""
        if self.next_calibration_date:
            delta = self.next_calibration_date - timezone.now()
            return delta.days
        return None

    def generate_status_report(self):
        """Funkcja generuje raport o stanie sprzętu"""
        return {
            "name": self.equipment_name,
            "status": self.get_status_display(),
            "days_until_calibration": self.days_until_next_calibration(),
            "last_maintenance": self.last_maintenance_date,
            "calibration_provider": self.calibration_provider.calib_prov_name if self.calibration_provider else None,
        }

    def clean(self):
        if self.price and self.price < 0:
            raise ValidationError('Price must by >0')
