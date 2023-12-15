from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden


class GroupRequiredMixin(LoginRequiredMixin, AccessMixin):
    """
    Миксин для проверки принадлежности пользователя к определенной группе.
    """

    group_required = None  # Укажите имя требуемой группы

    def dispatch(self, request, *args, **kwargs):
        if not self.group_required:
            return HttpResponseForbidden("Group is not specified.")
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.groups.filter(name=self.group_required).exists():
            return HttpResponseForbidden("User is not a member of the required group.")

        return super().dispatch(request, *args, **kwargs)
