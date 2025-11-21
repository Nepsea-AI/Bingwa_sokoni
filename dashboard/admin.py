from django.contrib import admin

# Register your models here.
from dashboard.models import Transaction, Token
from django.contrib.auth.models import User

admin.site.register(Transaction)

admin.site.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'expiry')