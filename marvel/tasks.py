from celery import shared_task


@shared_task
def auto_sc():
    print('here')
    return 'halo'
