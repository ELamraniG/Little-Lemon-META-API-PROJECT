from django.contrib.auth.models import Group


def ensureDefaultGroups():
    Group.objects.get_or_create(name='Manager')
    Group.objects.get_or_create(name='Delivery crew')


def isManager(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name='Manager').exists()


def isDeliveryCrew(user):
    return user.groups.filter(name='Delivery crew').exists()
