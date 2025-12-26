from datetime import date
from appointments.models import Appointment
from communications.models import CommunicationLog, CommunicationSettings

def send_appointment_reminders():
    today = date.today()

    appointments = Appointment.objects.filter(
        appointment_time__date=today,
        status='scheduled'
    )

    for appt in appointments:
        settings = CommunicationSettings.objects.filter(
            clinic=appt.clinic
        ).first()

        if not settings or not settings.send_appointment_reminders:
            continue

        message = (
            f"Reminder: You have an appointment at "
            f"{appt.clinic.name} today."
        )

        CommunicationLog.objects.create(
            clinic=appt.clinic,
            patient=appt.patient,
            appointment=appt,
            message_type='appointment_reminder',
            message_content=message
        )
