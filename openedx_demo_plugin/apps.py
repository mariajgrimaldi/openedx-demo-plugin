"""
openedx_demo_plugin Django application initialization.
"""

from django.apps import AppConfig


class OpenedxDemoPluginConfig(AppConfig):
    """
    Configuration for the openedx_demo_plugin Django application.
    """

    name = 'openedx_demo_plugin'

    plugin_app = {
        'signals_config': {
            'lms.djangoapp': {
                'relative_path': 'receivers',
                'receivers': [
                    {
                        'receiver_func_name': 'assign_org_course_access_to_user',
                        'signal_path': 'openedx_events.learning.signals.STUDENT_REGISTRATION_COMPLETED',
                    },
                ],
            }
        },
        'settings_config': {
            'lms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'devstack': {'relative_path': 'settings.devstack'},
            },
            'cms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'devstack': {'relative_path': 'settings.devstack'},
            },
        },
    }
