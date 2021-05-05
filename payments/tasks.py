from datetime import date

from celery.schedules import crontab

from miniblog import celery_app
from payments.models import MemberAccount


@celery_app.task
def check_subscribe(sub):
    for subscription, end_date in sub.items():
        if end_date == str(date.today()):
            MemberAccount.objects.filter(sub_id=subscription).update(
                account_type="Standard",
                subscription_end_date=None,
                active_subscription=False
            )


subscriptions = MemberAccount.objects.all()
sub = dict()
for subscription in subscriptions:
    sub[subscription.sub_id] = str(subscription.subscription_end_date)
print(sub)

celery_app.conf.beat_schedule = {
    'check_subscribe': {
        'task': 'payments.tasks.check_subscribe',
        'schedule': crontab(hour=00, minute=00),
        'args': (sub,),
    },
}
celery_app.conf.timezone = 'Europe/Kiev'

