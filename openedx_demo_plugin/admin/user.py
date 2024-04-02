"""User admin file.

Contains all the supported admin models for django.contrib.auth.model.User.

classes:
    ExportCsvMixin: Export data query in csv
    DemoUserAdmin: Extend UserAdmin behavior.
"""

import csv
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from openedx_demo_plugin.admin.register_admin_model import register_admin_model as register
from openedx_demo_plugin.edxapp_wrapper.student_module import UserAdmin


User = get_user_model()


class ExportCsvMixin:
    """Mixin for exporting queryset as CSV."""
    def export_as_csv(self, request, queryset):
        """Exports selected data to csv"""
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=users_data.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class EmailInfoFilter(admin.SimpleListFilter):
    """Filter for users who have opted to receive email info."""
    title = 'Receive Email information'
    parameter_name = 'receive_email_info'

    def lookups(self, request, model_admin):
        """Define filter lookups criteria."""
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        """Return queryset based on the class value."""
        if self.value() == 'yes':
            return queryset.filter(profile__meta__iexact='{"mktg": true}')
        elif self.value() == 'no':
            return queryset.filter(profile__meta__iexact='')

        return queryset

class DemoUserAdmin(UserAdmin, ExportCsvMixin):
    """Openedx demo site User admin class."""
    list_display = UserAdmin.list_display
    list_filter = UserAdmin.list_filter + (EmailInfoFilter,)
    search_fields = UserAdmin.search_fields
    fieldsets = UserAdmin.fieldsets
    actions = ["export_as_csv"]

register(User, DemoUserAdmin)
