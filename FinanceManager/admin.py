from django.contrib import admin
from .models import User, Category, Transaction, UserBalance

class Admin(admin.ModelAdmin):
    list_display = ("id", "username", "income", "category", "amount" "description")
    
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(UserBalance)