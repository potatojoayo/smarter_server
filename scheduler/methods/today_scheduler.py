from scheduler.methods import update_membership, attendance_management, absent_management
from scheduler.methods.student_payment import student_payment
from server.celery import app, logger


@app.task
def today_scheduler():
    try:
        logger.info("Starting today_scheduler")
        update_membership()
        attendance_management()
        # absent_management()
        student_payment()
        logger.info("finishing today_scheduler")
    except Exception as e:
        logger.error("Error in today_scheduler task: %s", e)
