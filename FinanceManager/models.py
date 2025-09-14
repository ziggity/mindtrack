from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=7, choices=CATEGORY_TYPE_CHOICES, default='expense')
    is_predefined = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name', 'category_type'], name='unique_category_for_user')
        ]

    def save(self, *args, **kwargs):
        if self.is_predefined:
            self.user = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category_type})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    transaction_type = models.CharField(max_length=7, choices=Category.CATEGORY_TYPE_CHOICES, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=225, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        category_type = self.category.category_type.capitalize() if self.category else "No Category"
        return f"{category_type} - {self.amount}"

class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from decimal import Decimal
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def update_balance(self, transaction):
        self.recalculate_balance()
        self.save()

    def recalculate_balance(self):
        transactions = Transaction.objects.filter(user=self.user)
        self.balance = sum(transaction.amount if transaction.transaction_type == 'income' else -transaction.amount for transaction in transactions)
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Balance: {self.balance}"

class RecurringTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)
    interval = models.CharField(max_length=20)
    next_occurrence = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} every {self.interval}"


