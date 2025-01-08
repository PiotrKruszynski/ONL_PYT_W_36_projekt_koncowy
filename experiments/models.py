from django.core.exceptions import ValidationError
from django.db import models
from equipment.models import Equipment
from samples.models import Sample
from users.models import Profile


TEST_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]

class Test(models.Model):
    test_name = models.CharField(max_length=200)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="test")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="tests_with_equipment")
    technician = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'technician'})
    lab_member = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'lab_member'})
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    result = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    standard = models.ForeignKey('ResearchStandard', on_delete=models.SET_NULL, null=True, blank=True)  # Relacja z modelem ResearchStandard
    status = models.CharField(
        max_length=20,
        choices=TEST_STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Test: {self.test_name} -- {self.status}"

    class Meta:
        ordering = ['-start_date']

    def clean(self):
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be later than start date.")

    @property
    def test_duration(self):
        """Czas trwania testów"""
        if self.start_date and self.end_date:
            return self.end_date - self.start_date
        return None

class ResearchStandard(models.Model):
    research_st_name = models.CharField(max_length=200, unique=True)
    method = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.research_st_name
