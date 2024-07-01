from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .forms import CustomAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm, IncomeForm
from .models import PAYMENT_METHOD
from django.db.models import Sum
import calendar
from  rest_framework.decorators import api_view
from  rest_framework.response import Response
from .serializers import ExpenseSerializer, IncomeSerializer





# Create your views here.
@api_view(['GET'])
def listIncome(request):
    inc = Income.objects.all()
    serializer = IncomeSerializer(inc, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def listExpense(request):
    exp = Expense.objects.all()
    serializer = ExpenseSerializer(exp, many=True)
    return Response(serializer.data)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = CustomAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                # Redirect to a success page after successful login
                return redirect('dashboard')  # Replace 'success_page' with the URL name of your success page
        else:
            form = CustomAuthenticationForm()

    # Render the login form template with the form
    return render(request, 'loginpage.html', {'form': form})

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                    form.save()
                    # Redirect to a success page after successful registration
                    return redirect('loginpage')  # Replace 'success_page' with the URL name of your success page
    

        # Render the registration form template with the form, even if it's not valid
        return render(request, 'registerpage.html', {'form': form})


def logoutpage(request):
    logout(request)
    return redirect('loginpage')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

@login_required(login_url='loginpage')
def dashboard(request):
    # Fetching data from Expense model for the chart
    expenses_data = Expense.objects.filter(user=request.user).values('date__month').annotate(total_amount=Sum('amount'))

    # Fetching data from Income model for the chart
    income_data = Income.objects.filter(user=request.user).values('date__month').annotate(total_amount=Sum('amount'))

    # Prepare sorted and formatted data for expenses and income
    sorted_expense_data = [0] * 12
    sorted_income_data = [0] * 12

    for entry in expenses_data:
        sorted_expense_data[entry['date__month'] - 1] = float(entry['total_amount'])

    for entry in income_data:
        sorted_income_data[entry['date__month'] - 1] = float(entry['total_amount'])

    # Calculate profit data
    profit_data = [round(income - expense, 2) for income, expense in zip(sorted_income_data, sorted_expense_data)]

    # Filter out months with zero data
    months_with_data = [
        calendar.month_abbr[month + 1] for month, (expense, income, profit) in enumerate(
            zip(sorted_expense_data, sorted_income_data, profit_data)
        )
        if expense > 0 or income > 0 or profit > 0
    ]
    filtered_expense_data = [amount for amount in sorted_expense_data if amount > 0]
    filtered_income_data = [amount for amount in sorted_income_data if amount > 0]
    filtered_profit_data = [amount for amount in profit_data if amount > 0]

    context = {
        'formatted_months': months_with_data,
        'sorted_expense_data': filtered_expense_data,
        'sorted_income_data': filtered_income_data,
        'sorted_profit_data': filtered_profit_data
    }
    
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total_exp=Sum('amount'))['total_exp']
    total_expenses = total_expenses if total_expenses is not None else 0

    total_income = Income.objects.filter(user=request.user).aggregate(total_inc=Sum('amount'))['total_inc']
    total_income = total_income if total_income is not None else 0

    profit = total_income - total_expenses

    context.update({'total_expenses': total_expenses, 'total_income': total_income, 'profit': profit})

    return render(request, 'dashboard.html', context)

##@login_required(login_url='loginpage')
def profile(request):
    return render(request, 'profile.html')

#@login_required(login_url='loginpage')
def listexpenses(request):

    expense = Expense.objects.filter(user=request.user) # Assuming Expense is your model name
    context = {
        'expense': expense,
    }

    return render(request, 'listexpenses.html', context)

@login_required(login_url='loginpage')
def addexpenses(request):
    form = ExpenseForm()
    expense = Expense.objects.all()
    payment_methods = [method[0] for method in PAYMENT_METHOD]
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            return redirect('listexpenses')

    context = {'form': form, 'expense': expense, 'payment_methods': payment_methods, 'categories': categories}
    return render(request, 'addexpenses.html', context)

@login_required(login_url='loginpage')
def updateexpenses(request, pk):

    expense = get_object_or_404(Expense, pk=pk, user=request.user) 
    form = ExpenseForm(instance=expense)
    payment_methods = [method[0] for method in PAYMENT_METHOD]
    categories = Category.objects.all()
    

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('listexpenses')

    context = {'form':form,'payment_methods':payment_methods,'categories':categories}
    return render(request, 'updateexpenses.html', context)

@login_required(login_url='loginpage')
def deleteexpense(request, pk):

    expense = get_object_or_404(Expense, pk=pk, user=request.user)
     
    if request.method == 'POST':
         expense.delete()
         return redirect('listexpenses')

    context={'expense':expense}
    return render(request, 'deleteexpense.html',context)



@login_required(login_url='loginpage')
def listincome(request):

    income = Income.objects.filter(user=request.user)  # Assuming Expense is your model name
    context = {
        'income': income,
    }

    return render(request, 'listincome.html', context)

@login_required(login_url='loginpage')
def addincome(request):
    form = IncomeForm()
    income = Income.objects.all()
    payment_methods = [method[0] for method in PAYMENT_METHOD]
    categories = Category.objects.all()

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save()
            return redirect('listincome')

    context = {'form': form, 'income': income, 'payment_methods': payment_methods, 'categories': categories}
    return render(request, 'addincome.html', context)

@login_required(login_url='loginpage')
def updateincome(request, pk):

    income = get_object_or_404(Income, pk=pk, user=request.user)
    form = IncomeForm(instance=income)
    payment_methods = [method[0] for method in PAYMENT_METHOD]
    categories = Category.objects.all()
    

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('listincome')

    context = {'form':form,'payment_methods':payment_methods,'categories':categories}
    return render(request, 'updateincome.html', context)

@login_required(login_url='loginpage')
def deleteincome(request, pk):

    income = get_object_or_404(Income, pk=pk, user=request.user)
     
    if request.method == 'POST':
         income.delete()
         return redirect('listincome')

    context={'income':income}
    return render(request, 'deleteincome.html',context)



@login_required(login_url='loginpage')
def invoice(request):
    return render(request, 'invoice.html')

def dashboardcharts(request):
    expenses = Expense.objects.filter(user=request.user)
    amounts = []
    dates = []
    for expense in expenses:
        amounts.append(expense.amount)
        dates.append(expense.date.strftime('%Y-%m-%d'))

    context = {'amounts': amounts, 'dates': dates}
    return render(request, 'dashboard.html', context)
