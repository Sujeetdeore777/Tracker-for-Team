from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.db.models import Sum  # Import Sum correctly here


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')




class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    hours_spent = models.DecimalField(max_digits=4, decimal_places=2)
    tags = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    manager_comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):

        self.hours_spent = Decimal(self.hours_spent)

        # Ensure that total hours for a given day do not exceed 8 for the same user.
        total_hours = Task.objects.filter(user=self.user, date=self.date).exclude(id=self.id).aggregate(
            Sum('hours_spent')
        )['hours_spent__sum'] or  Decimal(0)
        
        # Convert self.hours_spent to a float before performing the addition
        if total_hours + self.hours_spent > Decimal(8):
            raise ValueError("Total hours cannot exceed 8 per day.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
