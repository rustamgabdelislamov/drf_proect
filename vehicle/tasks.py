from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from vehicle.models import Car, Moto
from celery import shared_task


@shared_task
def check_milage(pk, model):
    if model == 'Car':
        instance = Car.objects.filter(pk=pk).first()
    else:
        instance = Moto.objects.filter(pk=pk).first()

    if instance:
        prev_milage = -1
        for m in instance.milage.all():
            if prev_milage == -1:
                prev_milage = m.milage
            else:
                if prev_milage < m.milage:
                    print('Неверный пробег')
                    break


@shared_task(name='vehicle.tasks.check_filter')
def check_filter():
    print('Task started')
    # filter_amount = {'amount__lte': 2000}

    # if Car.objects.filter(**filter_amount).exists():
    #     send_mail(
    #         subject='Отчет по фильтру',
    #         message='Есть машины',
    #         from_email=EMAIL_HOST_USER,
    #         recipient_list=[EMAIL_HOST_USER]
    #     )
