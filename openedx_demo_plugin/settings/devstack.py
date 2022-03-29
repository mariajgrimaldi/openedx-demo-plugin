"""
Devstack settings for the Open edX Demo site.
"""

def plugin_settings(settings):
    """
    Defines openedx-demo-plugin settings when app is used as a plugin to edx-platform.
    See: https://github.com/openedx/edx-django-utils/tree/master/edx_django_utils/plugins
    """
    settings.OPEN_EDX_VISITOR_ORG = "Public"
    settings.FEATURES['ENABLE_CREATOR_GROUP'] = True
