import django.dispatch

add_penalty = django.dispatch.Signal(providing_args=["user", "client", "penalty", "server"])
change_penalty = django.dispatch.Signal(providing_args=["user", "client", "penalty", "server"])
delete_penalty = django.dispatch.Signal(providing_args=["user", "client", "server"])
update_player_group = django.dispatch.Signal(providing_args=["user", "client", "server"])