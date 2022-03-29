"""
File where Open edX Events receivers are defined.

For a detailed description on events receivers definitions please refer to the
hooks official documentation.
"""
from django.conf import settings
from django.contrib.auth.models import User
from openedx_events.learning.data import UserData

try:
    from common.djangoapps.student.api import get_access_role_by_role_name
except ImportError:
    get_access_role_by_role_name = object


def assign_org_course_access_to_user(user: UserData, **kwargs):
    """
    Grant ORG course access role after a users registration over the organization
    configured in the OPEN_EDX_VISITOR_ORG setting if exists.
    """
    visitor_org = getattr(settings, "OPEN_EDX_VISITOR_ORG", None)
    if not visitor_org:
        return

    registered_user = User.objects.get(username=user.pii.username)
    org_content_creator_role = get_access_role_by_role_name("org_course_creator_group")
    org_content_creator_role(org=visitor_org).add_users(registered_user)
