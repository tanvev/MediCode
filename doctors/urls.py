from django.urls import path
from visits.views import doctor_visits, edit_visit
from labs.views import assign_lab
from vendors.views import assign_vendor
from .views import doctor_payouts

urlpatterns = [
    path('visits/', doctor_visits, name='doctor_visits'),
    path('visit/<int:visit_id>/', edit_visit, name='edit_visit'),
    path('visit/<int:visit_id>/lab/', assign_lab, name='assign_lab'),
    path('visit/<int:visit_id>/vendor/', assign_vendor, name='assign_vendor'),
    path('payouts/', doctor_payouts, name='doctor-payouts'),

]
