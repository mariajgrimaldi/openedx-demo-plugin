"""Wrapper student module file.

This contains all the required dependencies from student.

Attributes:
    backend: Imported student module by using the plugin settings.
"""
from importlib import import_module

from django.conf import settings

backend = import_module(settings.OPEN_EDX_STUDENT_BACKEND)

UserAdmin = backend.get_user_admin()
