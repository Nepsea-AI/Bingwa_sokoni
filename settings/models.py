from django.contrib.auth.models import User
from django.db import models
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sim_type = models.CharField(max_length=10, blank=True, null=True)
    sim_number = models.CharField(max_length=15, blank=True, null=True)
    device_id = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # auto-generate device ID if not set
        if not self.device_id:
            self.device_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    CATEGORY_CHOICES = [
        ('mpesa', 'M-PESA'),
        ('safaricom', 'Safaricom'),
        ('user', 'User'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    sent_by_user = models.BooleanField(default=False) #True if the user replied or sent the message
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender}: {self.body[:100]}"# preview first 100 chars
    
    #🧱 1️⃣ class Meta:
    #extra settings that affect how Django interacts with that table. it defines behaviors (like ordering, table name, verbose name, etc).

    #🕓 2️⃣ ordering = ['-timestamp']
    #This line tells Django: “Whenever I query this model, automatically order the results by timestamp in descending order (newest first).”
    #If you remove the minus (-), it orders oldest first.
    #So instead of writing this every time in your views:
    #Message.objects.all().order_by('-timestamp')

    #you can just write:

    #Message.objects.all()

    #💬 3️⃣ def __str__(self):
    #This defines what should be displayed when you print a model object or view it in the Django admin.
    #Without it, Django would show something generic like:

    #Message object (1)

    #But with it, you get something readable like:

    #MPESA: Confirmed. You have received Ksh 200.00...
    
    


