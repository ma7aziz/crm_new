from service.models import Service
from datetime import datetime, timedelta


def check_old_requests():
    print('check_old_requests ')
    services = Service.objects.all().filter(
        status = 'closed',
        created_at__lte = datetime.now()-timedelta(days=2)
    )
    for service in services :
        service.archive = True
        service.save()
        