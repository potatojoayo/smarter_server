from scheduler.methods import calculate_agencies, calculate_subcontractors
from scheduler.methods.create_student_payment import create_student_payment
from scheduler.methods.notification_alarm_send_again import notification_alarm_send_again
from scheduler.methods.today_scheduler import today_scheduler


def run():
    create_student_payment(month=7, day=15)
    create_student_payment(month=7, day=16)
    today_scheduler()
    calculate_agencies()
    calculate_subcontractors()
    notification_alarm_send_again()
