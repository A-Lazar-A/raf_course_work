from django.contrib.auth.mixins import AccessMixin


class GroupRequiredMixin(AccessMixin):
    """
    Миксин для проверки принадлежности пользователя к определенной группе.
    """

    group_required = None  # Укажите имя требуемой группы

    def dispatch(self, request, *args, **kwargs):
        if not self.group_required or not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.groups.filter(name=self.group_required).exists():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)