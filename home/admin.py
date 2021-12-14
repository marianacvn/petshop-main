from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.models import User

from .models import Product, Client, Service, Schedule


class ClientAdmin(admin.ModelAdmin):
    list_display = ["get_username", "cpf"]

    @display(ordering="user__username", description="nickname")
    def get_username(self, obj):
        return obj.user.username


class ClientInline(admin.StackedInline):
    model = Client


class UserAdmin(admin.ModelAdmin):
    search_fields = ["username", "email", "password"]
    list_display = ["username", "email", "client"]
    exclude = ['password']
    inlines = [ClientInline]


class ServiceAdmin(admin.ModelAdmin):
    search_fields = ["service", "description"]
    list_display = ["service", "description", "value"]


class ScheduleAdmin(admin.ModelAdmin):
    search_fields = ["service", "client"]
    list_display = ["service", "client", "date"]


admin.site.register(Product)
admin.site.register(Client, ClientAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Schedule, ScheduleAdmin)
