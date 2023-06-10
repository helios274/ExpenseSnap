from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Expense, Category
import json
from django.http import JsonResponse
from django.core.paginator import Paginator

def expense(request):
    if not request.user.is_authenticated:
        return render(request, "account/login-error.html")
    categories = Category.objects.all().order_by('name')
    expenses = Expense.objects.filter(user=request.user)
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get("page")
    page_object = Paginator.get_page(paginator, page_number)
    context = {"categories": categories, "expenses": expenses, "page_object": page_object }
    return render(request, "expense/expense.html", context)

def add_expense(request):
    if request.method == "POST":
        category = request.POST['category']
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        Expense.objects.create(
            user=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description,
        )
        messages.success(request, "Expense saved successfully")
        return redirect("expense")

def update_expense(request, id):
    if not request.user.is_authenticated:
        return render(request, "account/login-error.html")
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all().order_by('name')
    context = {"expense": expense, "categories": categories}

    if request.method == "GET":
        return render(request, "expense/update-expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]

        expense.user = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, "Expense updated successfully")

        return redirect("expense")

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed successfully")
    return redirect("expense")

def filter_expense(request):
    if request.method == "POST":
        categories = json.loads(request.body).get("categories")
        minAmount = json.loads(request.body).get("minAmount")
        maxAmount = json.loads(request.body).get("maxAmount")
        startDate = json.loads(request.body).get("startDate")
        endDate = json.loads(request.body).get("endDate")

        expenses = Expense.objects.filter(user=request.user)
        if categories:
            expenses = expenses.filter(category__in=categories)
        if minAmount:
            expenses = expenses.filter(amount__gte=minAmount)
        if maxAmount:
            expenses = expenses.filter(amount__lte=maxAmount)
        if startDate:
            expenses = expenses.filter(date__gte=startDate)
        if endDate:
            expenses = expenses.filter(date__lte=endDate)

        data = expenses.values()

        return JsonResponse(list(data), safe=False)

def search_expense(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        expenses = (
            Expense.objects.filter(amount__istartswith=search_str, user=request.user)
            | Expense.objects.filter(date__istartswith=search_str, user=request.user)
            | Expense.objects.filter(
                description__icontains=search_str, user=request.user
            )
            | Expense.objects.filter(category__icontains=search_str, user=request.user)
        )
        data = expenses.values()
        return JsonResponse(list(data), safe=False)