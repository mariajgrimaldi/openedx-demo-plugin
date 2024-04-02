"""
Common settings for the Open edX Demo site.
"""


def plugin_settings(settings):
    """
    Defines openedx-demo-plugin settings when app is used as a plugin to edx-platform.
    See: https://github.com/openedx/edx-django-utils/tree/master/edx_django_utils/plugins
    """
    settings.OPEN_EDX_VISITOR_ORG = "Public"
    settings.FEATURES["ENABLE_CREATOR_GROUP"] = True
    settings.OPEN_EDX_STUDENT_BACKEND = 'openedx_demo_plugin.edxapp_wrapper.backends.student_l_v1'
    settings.OPEN_EDX_FILTERS_CONFIG = {
        "org.openedx.learning.homepage.render.started.v1": {
            "fail_silently": False,
            "pipeline": [
                "openedx_demo_plugin.pipeline.FilterCoursesByOrganization"
            ]
        },
        "org.openedx.learning.catalog.render.started.v1": {
            "fail_silently": False,
            "pipeline": [
                "openedx_demo_plugin.pipeline.FilterCoursesByOrganization"
            ]
        }
    }

    if "cms.djangoapps.course_creators" not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS = settings.INSTALLED_APPS + ["cms.djangoapps.course_creators"]
