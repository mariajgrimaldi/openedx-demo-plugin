"""This file contains all test for the receivers.py file.

Classes:
    RegistrationCompletedReceiverTest: test registration event receiver.
"""
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from openedx_events.data import EventsMetadata
from openedx_events.learning.data import UserData, UserPersonalData
from openedx_events.learning.signals import STUDENT_REGISTRATION_COMPLETED

from openedx_demo_plugin.receivers import assign_org_course_access_to_user

User = get_user_model()


@override_settings(
    OPEN_EDX_VISITOR_ORG="Public", COURSE_CREATOR_ADMIN_ID="dummy-staff-user",
)
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
        self.staff = User.objects.create(username=settings.COURSE_CREATOR_ADMIN_ID, is_staff=True)

    @patch("openedx_demo_plugin.receivers.CourseCreator")
    @patch("openedx_demo_plugin.receivers.get_organization_by_short_name")
    def test_receiver_called_after_event(self, get_organization_by_short_name, course_creator):
        """
        Test that assign_org_course_access_to_user is called the correct information after sending
        STUDENT_REGISTRATION_COMPLETED event.
        """
        organization_id = 1
        get_organization_by_short_name.return_value = {
            "id": organization_id,
        }
        STUDENT_REGISTRATION_COMPLETED.connect(assign_org_course_access_to_user)

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        get_organization_by_short_name.assert_called_with(settings.OPEN_EDX_VISITOR_ORG)
        course_creator.assert_called_with(
            user=self.registered_user,
            state=course_creator.GRANTED,
            all_organizations=False,
        )
        course_creator.organizations.add.assert_called_with(organization_id)

    @override_settings(COURSE_CREATOR_ADMIN_ID="non-existent-user")
    @patch("openedx_demo_plugin.receivers.CourseCreator")
    @patch("openedx_demo_plugin.receivers.get_organization_by_short_name")
    def test_unexistent_course_creator_staff(self, get_organization_by_short_name, course_creator):
        """
        Test that stops when the user associated with COURSE_CREATOR_ADMIN_ID does not exist
        after sending STUDENT_REGISTRATION_COMPLETED event.
        """
        STUDENT_REGISTRATION_COMPLETED.connect(assign_org_course_access_to_user)

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        get_organization_by_short_name.assert_called_with(settings.OPEN_EDX_VISITOR_ORG)
        course_creator.assert_called_with(
            user=self.registered_user,
            state=course_creator.GRANTED,
            all_organizations=False,
        )
        course_creator.organizations.add.assert_not_called()

    @override_settings(COURSE_CREATOR_ADMIN_ID=None)
    @patch("openedx_demo_plugin.receivers.CourseCreator")
    @patch("openedx_demo_plugin.receivers.get_organization_by_short_name")
    def test_not_specified_course_creator_id(self, get_organization_by_short_name, course_creator):
        """
        Test that stops when COURSE_CREATOR_ADMIN_ID is not specified before sending STUDENT_REGISTRATION_COMPLETED
        event.
        """
        STUDENT_REGISTRATION_COMPLETED.connect(assign_org_course_access_to_user)

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        get_organization_by_short_name.assert_called_with(settings.OPEN_EDX_VISITOR_ORG)
        course_creator.assert_called_with(
            user=self.registered_user,
            state=course_creator.GRANTED,
            all_organizations=False,
        )
        course_creator.organizations.add.assert_not_called()

    @override_settings(OPEN_EDX_VISITOR_ORG=None)
    @patch("openedx_demo_plugin.receivers.CourseCreator")
    @patch("openedx_demo_plugin.receivers.get_organization_by_short_name")
    def test_receiver_noop(self, get_organization_by_short_name, course_creator):
        """
        Test that when OPEN_EDX_VISITOR_ORG is not defined then the receiver acts as
        a noop.
        """
        STUDENT_REGISTRATION_COMPLETED.connect(assign_org_course_access_to_user)

        STUDENT_REGISTRATION_COMPLETED.send_event(
            user=self.user,
        )

        get_organization_by_short_name.return_value.assert_not_called()
        course_creator.assert_not_called()
        course_creator.organizations.add.assert_not_called()
