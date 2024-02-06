from django.contrib import admin
from .models import User_info, Account_plan, Subscription_history, Privacy_policy


@admin.register(User_info)
class User_info_admin(admin.ModelAdmin):
    search_fields = ('',)


@admin.register(Account_plan)
class Account_plan_admin(admin.ModelAdmin):
    search_fields = ('',)
    list_display = ('user', 'plan', )


@admin.register(Subscription_history)
class Subscription_history_admin(admin.ModelAdmin):
    search_fields = ('',)
    list_display = ('date', 'user', 'plan', 'amount', 'status', )
    ordering = ('date',)


@admin.register(Privacy_policy)
class Privacy_policy(admin.ModelAdmin):
    search_fields = ('',)