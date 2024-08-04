from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task
from shop.channels.integrations.hepsiburada.integration import Integration
from shop.channels.models import Channel
from shop.channels.enums import ChannelType


def get_all_channel_ids(channel_type: ChannelType):
    return (Channel.objects.filter(channel_type=channel_type, is_active=True)
            .values_list('pk', flat=True))

@shared_task
def get_orders_cron(**kwargs: dict):
    for channel_id in get_all_channel_ids(ChannelType.hepsiburada):
        current_time = timezone.now()
        get_orders.delay(
            channel_id,
            start_date=current_time - timedelta(minutes=5),
            end_date=current_time
        )



@shared_task
def get_orders(channel_id, timespan=None,
               offset=0, limit=10,
               start_date=None, end_date=None, **kwargs):
    filter_params = {
        'limit': min(limit, 10)
    }

    if start_date and end_date:
        start_date_time = start_date.strftime("%Y-%m-%d %H:%M")
        filter_params['beginDate'] = start_date_time

        end_date_time = end_date.strftime("%Y-%m-%d %H:%M")
        filter_params['endDate'] = end_date_time
    else:
        filter_params['timespan'] = timespan

    page = 1
    while True:
        filter_params['offset'] = offset
        try:
            channel = Channel.objects.get(pk=channel_id)
            i = Integration(channel_id=channel.pk, conf=channel.conf)
            i.do_action(
                action='get_orders',
                **filter_params,
            )
        except Exception as e:
            raise e
        page += 1
        offset += limit

@shared_task
def update_orders(channel_id, orders, **kwargs):
    pass
