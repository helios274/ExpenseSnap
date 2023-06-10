from django.shortcuts import render
from expense.models import Expense
from income.models import Income
import json
from django.http import JsonResponse
import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from calendar import monthrange
from babel import numbers

def index(request):
    if not request.user.is_authenticated:
        return render(request, "index.html")
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)
    today = datetime.date.today()
    start_date = today.replace(day=1)
    end_date = today.replace(day=today.day)
    income_this_month = incomes.filter(date__range=(
        start_date, end_date)).aggregate(total=models.Sum('amount'))['total']
    expense_this_month = expenses.filter(date__range=(
        start_date, end_date)).aggregate(total=models.Sum('amount'))['total']
    income_this_month = income_this_month or 0
    expense_this_month = expense_this_month or 0
    savings_this_month = numbers.format_currency(income_this_month - expense_this_month, 'INR', locale="en_IN") 
    income_this_month = numbers.format_currency(income_this_month, 'INR', locale="en_IN")
    context = {"expenses": expenses, "incomes": incomes,
               "income_this_month": income_this_month, "expense_this_month": expense_this_month, "savings_this_month": savings_this_month}
    return render(request, "stats.html", context)


def stats_data(request):
    today = datetime.date.today()
    six_months_ago = today - relativedelta(months=6)
    data = {}

    # get last six months expenses
    expense = Expense.objects.filter(
        user=request.user, date__gte=six_months_ago, date__lte=today
    )

    # add six months number of expense and total expense amount
    data["expense_count"] = expense.count()
    data["expense_sum"] = expense.aggregate(
        models.Sum("amount"))["amount__sum"]

    # get category wise expense amount in six months
    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expense)))
    category_sum_dict = {}
    for category in category_list:
        expense_by_category = expense.filter(category=category)
        category_sum_dict[category] = expense_by_category.aggregate(
            models.Sum("amount"))["amount__sum"]
    data["expense_by_category"] = category_sum_dict

    # get monthly expenses and incomes for the last six months
    monthly_data = []
    for i in range(6):
        start_date = six_months_ago.replace(day=1)
        _, last_day = monthrange(start_date.year, start_date.month)
        end_date = start_date.replace(day=last_day)

        monthly_expense = Expense.objects \
            .filter(user=request.user, date__range=(start_date, end_date)) \
            .aggregate(total_expense=models.Sum('amount'))['total_expense']
        monthly_income = Income.objects \
            .filter(user=request.user, date__range=(start_date, end_date)) \
            .aggregate(total_income=models.Sum('amount'))['total_income']

        monthly_expense = monthly_expense or 0
        monthly_income = monthly_income or 0

        monthly_data.append({
            'month': start_date.strftime('%B'),
            'year': start_date.strftime('%Y'),
            'expense': monthly_expense,
            'income': monthly_income
        })

        six_months_ago += datetime.timedelta(days=last_day)

    data["monthly_data"] = monthly_data

    return JsonResponse(data, safe=False)


def filter_stats(request):
    if request.method == "POST":
        startDate = json.loads(request.body).get("startDate")
        endDate = json.loads(request.body).get("endDate")
        data = {}
        expense = Expense.objects.filter(user=request.user)

        # filter by date
        if startDate:
            expense = expense.filter(date__gte=startDate)
        if endDate:
            expense = expense.filter(date__lte=endDate)
        data["expense_count"] = expense.count()
        data["expense_sum"] = expense.aggregate(
            models.Sum("amount"))["amount__sum"]

        # get category wise expense amount for the given date range
        def get_category(expense):
            return expense.category
        category_list = list(set(map(get_category, expense)))
        category_sum_dict = {}
        for category in category_list:
            expense_by_category = expense.filter(category=category)
            category_sum_dict[category] = expense_by_category.aggregate(
                models.Sum("amount"))["amount__sum"]

        data["expense_by_category"] = category_sum_dict

        return JsonResponse(data, safe=False)

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)