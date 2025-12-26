from django.db.models import Sum, Count
from payments.models import Payment
from visits.models import Visit
from labs.models import LabAssignment
from vendors.models import VendorAssignment


def clinic_earnings(clinic, start=None, end=None):
    qs = Payment.objects.filter(visit__clinic=clinic)
    if start and end:
        qs = qs.filter(payment_date__range=[start, end])
    return qs.aggregate(total=Sum('paid_amount'))['total'] or 0


def doctor_wise_revenue(clinic):
    return (
        Payment.objects
        .filter(visit__clinic=clinic)
        .values('doctor__user__username')
        .annotate(total=Sum('paid_amount'))
        .order_by('-total')
    )


def payment_method_split(clinic):
    return (
        Payment.objects
        .filter(visit__clinic=clinic)
        .values('payment_method')
        .annotate(total=Sum('paid_amount'))
    )


def lab_workload(clinic):
    return (
        LabAssignment.objects
        .filter(visit__clinic=clinic)
        .values('lab__name')
        .annotate(count=Count('id'))
    )


def vendor_workload(clinic):
    return (
        VendorAssignment.objects
        .filter(visit__clinic=clinic)
        .values('vendor__name')
        .annotate(count=Count('id'))
    )
from django.db.models import Count
from django.db.models.functions import TruncDate, ExtractHour
from visits.models import Visit
def patients_per_day(clinic, start=None, end=None):
    qs = Visit.objects.filter(clinic=clinic)

    if start and end:
        qs = qs.filter(visit_start__date__range=[start, end])

    return (
        qs.annotate(day=TruncDate('visit_start'))
          .values('day')
          .annotate(count=Count('id'))
          .order_by('day')
    )
def new_vs_repeat(clinic):
    visits = Visit.objects.filter(clinic=clinic).order_by('visit_start')

    seen = set()
    new_count = 0
    repeat_count = 0

    for v in visits:
        if v.patient_id in seen:
            repeat_count += 1
        else:
            new_count += 1
            seen.add(v.patient_id)

    return {
        'new': new_count,
        'repeat': repeat_count
    }
def busiest_hours(clinic):
    return (
        Visit.objects
        .filter(clinic=clinic)
        .annotate(hour=ExtractHour('visit_start'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
def busiest_days(clinic):
    return (
        Visit.objects
        .filter(clinic=clinic)
        .annotate(day=TruncDate('visit_start'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
def growth_percentage(current, previous):
    if previous == 0:
        return None
    return round(((current - previous) / previous) * 100, 2)
from expenses.models import Expense
from django.db.models import Sum

def total_expenses(clinic):
    return (
        Expense.objects
        .filter(clinic=clinic)
        .aggregate(total=Sum('amount'))['total'] or 0
    )

def net_profit(clinic):
    income = clinic_earnings(clinic)
    cost = total_expenses(clinic)
    return income - cost

from doctors.models import DoctorPayout

def doctor_margin(clinic):
    revenue = (
        Payment.objects
        .filter(visit__clinic=clinic)
        .values('doctor__user__username')
        .annotate(total_revenue=Sum('paid_amount'))
    )

    payouts = (
        DoctorPayout.objects
        .filter(clinic=clinic)
        .values('doctor__user__username')
        .annotate(total_payout=Sum('amount'))
    )

    payout_map = {
        p['doctor__user__username']: p['total_payout']
        for p in payouts
    }

    result = []
    for r in revenue:
        payout = payout_map.get(r['doctor__user__username'], 0)
        result.append({
            'doctor': r['doctor__user__username'],
            'revenue': r['total_revenue'],
            'payout': payout,
            'margin': r['total_revenue'] - payout
        })

    return result
