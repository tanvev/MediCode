from clinics.models import ClinicMembership


def get_user_role(user, clinic):
    try:
        membership = ClinicMembership.objects.get(
            user=user,
            clinic=clinic,
            is_active=True
        )
        return membership.role
    except ClinicMembership.DoesNotExist:
        return None
