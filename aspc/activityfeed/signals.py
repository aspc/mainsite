import django.dispatch

new_activity = django.dispatch.Signal(providing_args=["category", "date"])
delete_activity = django.dispatch.Signal()