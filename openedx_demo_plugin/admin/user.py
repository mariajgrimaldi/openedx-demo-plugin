"""User admin file.

Contains all the supported admin models for django.contrib.auth.model.User.

classes:
    ExportCsvMixin: Export data query in csv
    DemoUserAdmin: Extend UserAdmin behavior.
"""

import csv
import json

from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth import get_user_model
from openedx_demo_plugin.admin.register_admin_model import register_admin_model as register
from openedx_demo_plugin.edxapp_wrapper.student_module import UserAdmin

User = get_user_model()

class ExportCsvMixin:
    """Mixin for exporting queryset as CSV."""
    def export_as_csv(self, request, queryset, fields=None):
        """Exports selected data to CSV."""
        query = queryset.select_related('profile').all()

        user_fields = ['username', 'first_name', 'last_name', 'email']
        profile_fields = ['country', 'phone_number']

        field_names = fields if fields else user_fields + profile_fields

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=users_data.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in query:
            row = [getattr(obj.profile, field, '') if field in profile_fields and obj.profile else getattr(obj, field, '') for field in field_names]
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export Selected"


class EmailInfoFilter(admin.SimpleListFilter):
    """Openedx demo site filter receive info."""
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
        meta_queryset = queryset.exclude(profile__isnull=True).exclude(profile__meta='').values('profile__meta')
        empty_queryset = queryset.exclude(profile__isnull=True).filter(profile__meta__iexact='')
        meta_true = []
        meta_false = []

        for elem in meta_queryset:
            try:
                meta_data = json.loads(elem['profile__meta'])

                mktg_value = meta_data.get('mktg')
                if mktg_value is not None:
                    if mktg_value == 'true':
                        meta_true.append(elem['profile__meta'])
                    else:
                        meta_false.append(elem['profile__meta'])

            except json.decoder.JSONDecodeError:
                pass

        if self.value() == 'yes':
            return queryset.filter(profile__meta__in=meta_true)
        elif self.value() == 'no':
            return empty_queryset | queryset.filter(profile__meta__in=meta_false)

        return queryset


class DemoUserAdmin(UserAdmin, ExportCsvMixin):
    """Openedx demo site User admin class."""
    list_display = UserAdmin.list_display
    list_filter = UserAdmin.list_filter + (EmailInfoFilter,)
    search_fields = UserAdmin.search_fields
    fieldsets = UserAdmin.fieldsets
    actions = ["export_as_csv"]

register(User, DemoUserAdmin)
