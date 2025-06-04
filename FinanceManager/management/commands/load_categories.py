from django.core.management.base import BaseCommand
from FinanceManager.models import Category

class Command(BaseCommand):
    help = 'Load predefined income and expense categories into the database'

    def handle(self, *args, **kwargs):
        income_categories = [
            'Salary/Wages',
            'Freelance/Contract Work',
            'Business Income',
            'Investment Income',
            'Rental Income',
            'Bonuses',
            'Commission',
            'Pension',
            'Retirement Account Withdrawals',
            'Tax Refund',
            'Gift Received',
            'Scholarship/Grant',
            'Lottery/Prize Winnings',
            'Child Support Received',
            'Government Benefits',
        ]

        expense_categories = [
            'Rent',
            'Mortgage',
            'Property Taxes',
            'Home Insurance',
            'Home Maintenance/Repairs',
            'Utilities',
            'Car Payment',
            'Car Insurance',
            'Fuel/Gas',
            'Healthcare',
            'Education',
            'Entertainment',
            'Debt Payments',
            'Savings & Investments',
            'Family & Childcare',
            'Personal Care',
            'Charity & Donations',
            'Miscellaneous',
        ]

        # Load income categories
        for category_name in income_categories:
            category, created = Category.objects.get_or_create(
                name=category_name,
                category_type='income',
                defaults={'is_predefined': True}
            )
            if not created:
                category.is_predefined = True  # Update predefined status if necessary
                category.save()

        # Load expense categories
        for category_name in expense_categories:
            category, created = Category.objects.get_or_create(
                name=category_name,
                category_type='expense',
                defaults={'is_predefined': True}
            )
            if not created:
                category.is_predefined = True  # Update predefined status if necessary
                category.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded predefined categories.'))
