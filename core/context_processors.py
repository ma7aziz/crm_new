
from users.models import User

def context(request):
    ctx = {
        'companies': User.objects.filter(role='company')
    }
    
    return ctx