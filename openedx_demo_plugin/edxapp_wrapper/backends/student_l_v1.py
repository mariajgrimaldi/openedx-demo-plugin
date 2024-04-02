"""Backend for student module.

This file contains all the necessary student dependencies from
https://github.com/eduNEXT/edunext-platform/tree/master/common/djangoapps/student
"""
from common.djangoapps.student.admin import \
    UserAdmin  # pylint: disable=import-error, no-name-in-module, useless-suppression


def get_user_admin():
    """Allow to get UserAdmin model
    https://github.com/eduNEXT/edunext-platform/tree/master/common/djangoapps/student/admin.py

    Returns:
        UserAdmin model.
    """
    return UserAdmin
