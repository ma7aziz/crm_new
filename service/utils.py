from datetime import datetime

from django.db.models import Max

from . import models

def generate_ref_number(service_type):

    prefix = 'INS' if service_type == 'install' else 'REP'
    year = str(datetime.now().year)[-2:]

    last_ref_number = models.Service.objects.filter(
        ref_number__startswith=f'{prefix}{year}'
    ).aggregate(Max('ref_number'))['ref_number__max']

    if not last_ref_number:
        return f'{prefix}{year}001'

    last_number = int(last_ref_number[-3:])
    new_number = f'{last_number+1:03d}'
    return f'{prefix}{year}{new_number}'
