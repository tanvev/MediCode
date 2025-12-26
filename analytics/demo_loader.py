from datetime import date, timedelta
import random

from clinics.models import Clinic, ClinicMembership
from doctors.models import DoctorProfile, DoctorPayout
from patients.models import Patient
from visits.models import Visit
from appointments.models import Appointment
from payments.models import Payment
from expenses.models import Expense
from django.contrib.auth import get_user_model

User = get_user_model()


def load_demo_data(owner_user):
    """
    ⚠️ CALL ONLY IN DEMO MODE
    """

    # 1️⃣ Clinic
    clinic, _ = Clinic.objects.get_or_create(
        name="MediCode Demo Clinic",
        specialty="dental"
    )

    ClinicMembership.objects.get_or_create(
        user=owner_user,
        clinic=clinic,
        role="owner",
        is_active=True
    )

    # 2️⃣ Doctors
    doctors = []
    for name in ["Dr. Asha", "Dr. Rohit"]:
        email = name.lower().replace(" ", "") + "@demo.com"
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0]}
        )

        doctor, _ = DoctorProfile.objects.get_or_create(
            user=user,
            clinic=clinic,
            specialization="Dental",
            is_owner=(name == "Dr. Asha")
        )
        doctors.append(doctor)

    # 3️⃣ Patients + Visits + Payments
    for i in range(15):
        patient = Patient.objects.create(
            clinic=clinic,
            name=f"Patient {i+1}",
            phone=f"90000000{i}"
        )

        visit_date = date.today() - timedelta(days=random.randint(0, 20))

        visit = Visit.objects.create(
            clinic=clinic,
            patient=patient,
            doctor=random.choice(doctors),
            visit_start=visit_date
        )

        Payment.objects.create(
            visit=visit,
            doctor=visit.doctor,
            billed_amount=1000,
            paid_amount=random.choice([800, 1000]),
            payment_method=random.choice(["cash", "upi"])
        )

    # 4️⃣ Expenses
    Expense.objects.bulk_create([
        Expense(
            clinic=clinic,
            category="rent",
            amount=15000,
            expense_date=date.today().replace(day=1)
        ),
        Expense(
            clinic=clinic,
            category="staff",
            amount=20000,
            expense_date=date.today().replace(day=1)
        )
    ])

    # 5️⃣ Doctor payouts
    for d in doctors:
        DoctorPayout.objects.create(
            doctor=d,
            clinic=clinic,
            month=date.today().replace(day=1),
            amount=random.choice([12000, 18000])
        )

    return clinic
