"""
File where Open edX filters pipeline steps are defined.

For a detailed description on filters definitions please refer to the
hooks official documentation.
"""
from django.conf import settings
from openedx_filters import PipelineStep


class FilterCoursesByOrganization(PipelineStep):
    """
    Filter courses rendered in the current template context based on the OPEN_EDX_VISITOR_ORG
    setting.

    "OPEN_EDX_FILTERS_CONFIG": {
        "org.openedx.learning.homepage.render.started.v1": {
            "fail_silently": false,
            "pipeline": [
                "openedx_demo_plugin.pipeline.FilterCoursesByOrganization"
            ]
        },
        "org.openedx.learning.catalog.render.started.v1": {
            "fail_silently": false,
            "pipeline": [
                "openedx_demo_plugin.pipeline.FilterCoursesByOrganization"
            ]
        }
    },
    """

    def run_filter(self, context, template_name, *args, **kwargs):  # pylint: disable=arguments-differ
        visitor_org = getattr(settings, "OPEN_EDX_VISITOR_ORG", None)
        if not visitor_org:
            return {}
        context["courses"] = [course for course in context["courses"] if course.org != visitor_org]
        return {
            "context": context,
        }
