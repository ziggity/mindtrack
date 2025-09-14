from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User, Transaction, Category, UserBalance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.db.models import Sum
from django.urls import reverse
import json



def index(request):
    transactions = []
    balance = 0
    total_income = 0
    total_expenses = 0

    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
        balance = calculate_balance(transactions)

        # Calculate total income and expenses
        total_income = transactions.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = transactions.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    paginator = Paginator(transactions, 2)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'FinanceManager/index.html', {
        'transactions': transactions,
        'page_obj': page_obj,
        'balance': balance,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'is_authenticated': request.user.is_authenticated
    })


def calculate_balance(transactions):
    income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    return income - expense


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "FinanceManager/login.html", {
                "message": "Invalid Username and/or Password"
            })
    return render(request, "FinanceManager/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if not username or not email or not password or not confirmation:
            return render(request, "FinanceManager/register.html", {
                "error": "All fields are required."
            })

        if password != confirmation:
            return render(request, "FinanceManager/register.html", {"error": "Passwords must match."})

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return JsonResponse({"error": "Username already taken."}, status=400)

        login(request, user)
        return HttpResponseRedirect(reverse("login"))
        

    return render(request, "FinanceManager/register.html")


@login_required
def get_categories(request, transaction_type):
    categories = Category.objects.filter(category_type=transaction_type)
    categories_data = [{"id": category, "name": category.name} for category in categories]
    return JsonResponse({"categories": categories_data})


@login_required
def add_transaction(request):
    if request.method == "POST":
        try:
            amount = request.POST.get('amount')
            if not amount:
                return JsonResponse({"error": "Amount is required."}, status=400)

            try:
                amount = float(amount)
                if amount <= 0:
                    return JsonResponse({"error": "Amount must be greater than zero."}, status=400)
            except ValueError:
                return JsonResponse({"error": "Invalid amount format."}, status=400)

            transaction_type = request.POST.get('transaction_type')
            if transaction_type not in ['income', 'expense']:
                return JsonResponse({"error": "Invalid transaction type."}, status=400)

            description = request.POST.get('description')
            category_id = request.POST.get('category')

            try:
                category = Category.objects.get(id=category_id, category_type=transaction_type)
            except Category.DoesNotExist:
                return JsonResponse({"error": "Invalid category for the selected transaction type."}, status=400)

            transaction = Transaction.objects.create(
                user=request.user,
                category=category,
                amount=amount,
                description=description,
                transaction_type=transaction_type
            )

            user_balance, created = UserBalance.objects.get_or_create(user=request.user)
            user_balance.update_balance(transaction)

        except ValueError as e:
            return JsonResponse({"error": f"Invalid input: {str(e)}"}, status=400)

    categories = Category.objects.all()
    return render(request, "FinanceManager/add_transaction.html", {
        "categories": categories
    })


@login_required
def transaction_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    transaction = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(transaction, 5)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "FinanceManager/transactions.html", {
        "page_obj": page_obj,
        "balance": calculate_balance(transaction),
    })


