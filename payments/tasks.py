from datetime import date

from celery.schedules import crontab

from miniblog import celery_app
from payments.models import MemberAccount


@celery_app.task
def check_subscribe():
    subscriptions = MemberAccount.objects.filter(active_subscription=True, subscription_end_date__lte=date.today())\
        .update(
            account_type="Standard",
            subscription_end_date=None,
            active_subscription=False
        )
    print(subscriptions)
