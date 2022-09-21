"""
File where Open edX Events receivers are defined.

For a detailed description on events receivers definitions please refer to the
hooks official documentation.
"""
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from openedx_events.learning.data import UserData

try:
    from cms.djangoapps.course_creators.models import CourseCreator
    from organizations.api import get_organization_by_short_name
except ImportError:
    get_organization_by_short_name = object
    CourseCreator = object

User = get_user_model()
log = logging.getLogger(__name__)


def assign_org_course_access_to_user(user: UserData, **kwargs):
    """
    Grant ORG course access role after a users registration.

    This permission is granted over the organization configured in the
    OPEN_EDX_VISITOR_ORG setting if exists. If doesn't exist, then acts
    like a noop.
    """
    visitor_org_short_name = getattr(settings, "OPEN_EDX_VISITOR_ORG", None)
    if not visitor_org_short_name:
        return
    visitor_org = get_organization_by_short_name(visitor_org_short_name)

    registered_user = User.objects.get(username=user.pii.username)
    course_creator = CourseCreator(
        user=registered_user,
        state=CourseCreator.GRANTED,
        all_organizations=False,
    )

    # In order to add course creator permissions programmatically, we must attach
    # to the user just registered. So the post_add signals receivers like
    # `course_creator_organizations_changed_callback` can run checks over instance.admin.
    try:
        course_creator.admin = User.objects.get(username=settings.COURSE_CREATOR_ADMIN_ID)
    except User.DoestNotExist:
        log.exception("User with username specified in COURSE_CREATOR_ADMIN_ID does not exist.")
        return
    course_creator.save()
    course_creator.organizations.add(visitor_org.get("id"))
