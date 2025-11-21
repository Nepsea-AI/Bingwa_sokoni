from django.db import models

# Create your models here.

# models.py

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    SIM_CHOICES = [
        ('sim1', 'Sim1'),
        ('sim2', 'Sim2'),
        
    ]

    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    package_type = models.CharField(max_length=50)
    sim_slot = models.CharField(max_length=10, choices=SIM_CHOICES, default='sim1')
    ussd_string = models.CharField(max_length=100)
    sender = models.CharField(max_length=50, default='MPESA')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"



class Token(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry = models.CharField(max_length=50, default="No Expiry")

    def __str__(self):
        return f"{self.name} - Ksh {self.price}"
