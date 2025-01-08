from django.db import models
from django.utils.timezone import now

# Create your models here.
SAMPLE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
]

class Sample(models.Model):
    sample_id = models.CharField(max_length=20, unique=True)  # Unikalny identyfikator
    sample_name = models.CharField(max_length=100)  # Nazwa próbki lub wyrobu bud.
    description = models.TextField(blank=True, null=True)  # Opcjonalny opis próbki
    collected_by = models.ForeignKey(
        'Profile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='collected_samples'
    )  # Powiązanie z użytkownikiem potwierdzającym pobranie
    assigned_to = models.ForeignKey(
        'Profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_samples'
    )  # Powiązanie z użytkownikiem odpowiedzialnym za próbkę
    status = models.CharField(
        max_length=20,
        choices=SAMPLE_STATUS_CHOICES,
        default='pending'
    )  # Status próbki
    collection_date = models.DateTimeField(default=now)  # Data pobrania próbki
    completion_date = models.DateTimeField(blank=True, null=True)  # Data zakończenia pracy z próbką
    notes = models.TextField(blank=True, null=True)  # Dodatkowe notatki

    def __str__(self):
        return f"Sample {self.sample_id} - {self.sample_name}"

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completion_date:
            self.completion_date = now()
        super().save(*args, **kwargs)