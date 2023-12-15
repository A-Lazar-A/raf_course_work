from django.contrib import admin


from main_app.models import User, Department, SupportRequest

# class AdminUser(UserAdmin):
#     model = UserAdmin
admin.site.register(User)
# admin.site.register(TimeTracking)
admin.site.register(Department)
admin.site.register(SupportRequest)
# admin.site.register(Device)

# Register your models here.
