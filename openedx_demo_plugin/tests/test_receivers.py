"""This file contains all test for the receivers.py file.

Classes:
    RegistrationCompletedReceiverTest: test registration event receiver.
"""
import datetime
from unittest.mock import patch

from django.test import TestCase, override_settings
from opaque_keys.edx.keys import CourseKey
from openedx_events.data import EventsMetadata
from openedx_events.learning.data import CourseData, CourseEnrollmentData, UserData, UserPersonalData
from openedx_events.learning.signals import COURSE_ENROLLMENT_CREATED, STUDENT_REGISTRATION_COMPLETED
from django.contrib.auth.models import User

from openedx_demo_plugin.receivers import assign_org_course_access_to_user


class RegistrationCompletedReceiverTest(TestCase):
    """
    Tests the registration receiver assigns the correct permissions.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.user = UserData(
            pii=UserPersonalData(
                username="test",
                email="test@example.com",
                name="Test Example",
            ),
            id=39,
            is_active=True,
        )
        self.metadata = EventsMetadata(
            event_type="org.openedx.learning.student.registration.completed.v1",
            minorversion=0,
        )
        self.registered_user = User.objects.create(username=self.user.pii.username)

    @override_settings(OPEN_EDX_VISITOR_ORG="demo")
    @patch("openedx_demo_plugin.receivers.get_access_role_by_role_name")
    def test_receiver_called_after_event(self, get_access_role_by_role_name):
        """
        Test that assign_org_course_access_to_user is called the correct information after sending
        STUDENT_REGISTRATION_COMPLETED event.
        """
        org_content_creator_role = get_access_role_by_role_name("org_course_creator_group")
        STUDENT_REGISTRATION_COMPLETED.connect(assign_org_course_access_to_user)

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        org_content_creator_role(org="demo").add_users.assert_called_with(self.registered_user)

    @override_settings(OPEN_EDX_VISITOR_ORG=None)
    @patch("openedx_demo_plugin.receivers.get_access_role_by_role_name")
    def test_receiver_noop(self, get_access_role_by_role_name):
        """
        Test that when OPEN_EDX_VISITOR_ORG is not defined then the receiver acts as
        a noop.
        """
        STUDENT_REGISTRATION_COMPLETED.connect(assign_org_course_access_to_user)

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        get_access_role_by_role_name.return_value.assert_not_called()
