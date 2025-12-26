from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from clinics.models import Clinic
from permissions.utils import get_user_role

@login_required
def expense_list(request):
    clinic = Clinic.objects.first()

    if get_user_role(request.user, clinic) != 'owner':
        return redirect('/login/')

    if request.method == 'POST':
        Expense.objects.create(
            clinic=clinic,
            category=request.POST['category'],
            amount=request.POST['amount'],
            description=request.POST.get('description', ''),
            expense_date=request.POST['date']
        )
        return redirect('expenses')

    expenses = Expense.objects.filter(clinic=clinic).order_by('-expense_date')

    return render(request, 'expenses/expenses.html', {
        'expenses': expenses
    })
