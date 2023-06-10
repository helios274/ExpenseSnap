from django.shortcuts import render, redirect
from . models import Income, Source
from django.core.paginator import Paginator
from django.contrib import messages
import json
from django.http import JsonResponse

def income(request):
    if not request.user.is_authenticated:
        return render(request, "account/login-error.html")
    sources = Source.objects.all().order_by("name")
    incomes = Income.objects.filter(user=request.user)
    paginator = Paginator(incomes, 10)
    page_number = request.GET.get("page")
    page_object = Paginator.get_page(paginator, page_number)
    context = {"sources": sources, "incomes": incomes, "page_object": page_object}
    return render(request, "income/income.html", context)

def add_income(request):
    if request.method == "POST":
        source = request.POST['source']
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        Income.objects.create(
            user=request.user,
            amount=amount,
            date=date,
            source=source,
            description=description,
        )
        messages.success(request, "Income saved successfully")
        return redirect("income")
    
def update_income(request, id):
    if not request.user.is_authenticated:
        return render(request, "account/login-error.html")
    income = Income.objects.get(pk=id)
    sources = Source.objects.all().order_by('name')
    context = {"income": income, "sources": sources}

    if request.method == "GET":
        return render(request, "income/update-income.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["income_date"]
        source = request.POST["source"]

        income.user = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, "Income updated successfully")

        return redirect("income")

def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income removed successfully")
    return redirect("income")

def filter_income(request):
    if request.method == "POST":
        sources = json.loads(request.body).get("sources")
        minAmount = json.loads(request.body).get("minAmount")
        maxAmount = json.loads(request.body).get("maxAmount")
        startDate = json.loads(request.body).get("startDate")
        endDate = json.loads(request.body).get("endDate")

        incomes = Income.objects.filter(user=request.user)
        if sources:
            incomes = incomes.filter(source__in=sources)
        if minAmount:
            incomes = incomes.filter(amount__gte=minAmount)
        if maxAmount:
            incomes = incomes.filter(amount__lte=maxAmount)
        if startDate:
            incomes = incomes.filter(date__gte=startDate)
        if endDate:
            incomes = incomes.filter(date__lte=endDate)

        data = incomes.values()

        return JsonResponse(list(data), safe=False)

def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        incomes = (
            Income.objects.filter(amount__istartswith=search_str, user=request.user)
            | Income.objects.filter(date__istartswith=search_str, user=request.user)
            | Income.objects.filter(
                description__icontains=search_str, user=request.user
            )
            | Income.objects.filter(source__icontains=search_str, user=request.user)
        )
        data = incomes.values()
        return JsonResponse(list(data), safe=False)
