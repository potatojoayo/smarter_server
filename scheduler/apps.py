from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from server import settings

job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'replace_existing': True
}

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE, job_defaults=job_defaults)


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self):
        from django_apscheduler.jobstores import DjangoJobStore
        scheduler.add_jobstore(DjangoJobStore(), 'default')
        scheduler.start()



    # def ready(self):
    #     from scheduler.methods.run_schedulers import run_schedulers
    #     print('apapapapap')
    #     run_schedulers()
