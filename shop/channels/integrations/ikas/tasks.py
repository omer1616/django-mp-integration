from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task
from .integration import Integration
from shop.channels.models import Channel
from shop.channels.enums import ChannelType


def get_all_channel_ids(channel_type: ChannelType):
    return (Channel.objects.filter(channel_type=channel_type, is_active=True)
            .values_list('pk', flat=True))


@shared_task
def get_orders_cron(**kwargs: dict):
    for channel_id in get_all_channel_ids(ChannelType.ikas):
        current_time = timezone.now()
        get_orders.delay(
            channel_id,
            start_date=current_time - timedelta(minutes=5),
            end_date=current_time
        )


def get_orders(channel_id, limit,  page=10,
               orderedAt_gt=None,  orderedAt_lt=None, **kwargs):
    start_date = orderedAt_gt.strftime("%Y-%m-%d %H:%M")
    end_date_time = orderedAt_lt.strftime("%Y-%m-%d %H:%M")

    variables = {
        "branchId": {
            "eq": str(channel_id)
        },
        "orderedAt": {
            "gt": start_date,
            "lt": end_date_time,
        },
        "pagination": {
            "limit": limit,
            "page": page
        }
    }
    kwargs.update(**variables)
    page, total_page = 0, 1
    while page < total_page:

        try:
            channel = Channel.objects.get(pk=channel_id)
            i = Integration(channel_id=channel.pk, conf=channel.conf)
            total_page = i.do_action(
                action='get_orders',
                **kwargs,
            )
        except Exception as e:
            total_page += 1
            raise e
        page += 1
        variables['pagination']['page'] = page


def update_orders(channel_id, orders, **kwargs):
    pass
