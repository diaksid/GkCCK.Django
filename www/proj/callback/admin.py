from django.contrib import admin
from django import forms

from proj.admin.filters import SiteListFilter

from .models import Order


class OrderModelAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'col-xs-7',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'col-xs-5',
            }),
            'site': forms.Select(attrs={
                'class': 'col-xs-5',
            }),
            'state': forms.NullBooleanSelect(attrs={
                'class': 'col-xs-2',
            }),
            'note': forms.Textarea(attrs={
                'rows': 3,
                'class': 'col-xs-7',
            }),
            'agent': forms.Select(attrs={
                'class': 'col-xs-5',
            }),
        }


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):

    date_hierarchy = 'sent_date'
    ordering = (
        '-state',
        '-sent_date',
        'site',
    )

    search_fields = (
        'name',
        'phone',
    )
    list_display = (
        'get_state',
        'get_date',
        'phone',
        'name',
        'get_site',
    )
    list_display_links = (
        'phone',
        'name',
    )
    list_filter = (
        'state',
        SiteListFilter,
    )

    form = OrderModelAdminForm
    fieldsets = (
        ('Заказ', {'fields': [
            'sent_date',
            'site',
        ]}),
        ('Данные', {'fields': [
            'name',
            'phone',
        ]}),
        ('Выполнение', {'fields': [
            'state',
            'note',
            'agent',
        ]}),
    )
    readonly_fields = (
        'sent_date',
        'site',
        'name',
        'phone',
        'agent',
    )

    def save_model(self, request, obj, form, change):
        if change:
            if obj._loaded_values['state'] != obj.state:
                obj.agent = request.user
                self.message_user(request, 'Присвоен идентефикатор агента', 'INFO')
        super(OrderModelAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        return ('sent_date',) if request.user.is_superuser else self.readonly_fields

    def get_date(self, instance):
        return instance.sent_date.strftime('%d.%m.%Y &nbsp; [%H:%M]')
    get_date.short_description = 'дата'
    get_date.admin_order_field = 'sent_date'
    get_date.allow_tags = True

    def get_state(self, instance):
        return instance.state
    get_state.short_description = 'звонок'
    get_state.admin_order_field = 'state'
    get_state.boolean = True

    def get_site(self, instance):
        return instance.site.name
    get_site.short_description = 'сайт'
    get_site.admin_order_field = 'site'
