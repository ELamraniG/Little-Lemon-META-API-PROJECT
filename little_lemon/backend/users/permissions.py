from django.contrib.auth.models import Group


def ensure_default_groups():
    Group.objects.get_or_create(name='Manager')
    Group.objects.get_or_create(name='Delivery crew')


def user_is_manager(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name='Manager').exists()


def user_is_delivery_crew(user):
    return user.groups.filter(name='Delivery crew').exists()
