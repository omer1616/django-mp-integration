from datetime import timedelta
CELERY_BEAT_SCHEDULE = {
    {
        'hepsiburada-get-orders-cron': {
            'task': 'shop.channels.integrations.hepsiburada.tasks.get_orders_cron',
            'schedule': timedelta(minutes=10),
            'args': ()
        }
    },
    {
        'hepsiburada-get-orders-cron': {
            'task': 'shop.channels.integrations.hepsiburada.tasks.get_orders_status_cron',
            'schedule': timedelta(minutes=10),
            'args': ()
        }
    },
    {
        'ikas-get-orders-cron': {
            'task': 'shop.channels.integrations.ikas.tasks.get_orders_cron',
            'schedule': timedelta(minutes=10),
            'args': ()
        }
    },
    {
        'ikas-get-orders-cron': {
            'task': 'shop.channels.integrations.ikas.tasks.get_orders_status_cron',
            'schedule': timedelta(minutes=10),
            'args': ()
        }
    }
}
