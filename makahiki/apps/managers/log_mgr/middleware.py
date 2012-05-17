"""A middleware class to support logging of interactions with logged in users."""
import traceback
from django.core.signals import got_request_exception
from django.dispatch.dispatcher import receiver
import re


# Filter out requests to media and site_media.
from apps.managers.log_mgr import log_mgr

MEDIA_REGEXP = r'^\/(site_)?media'
SENTRY_REGEXP = r'^\/sentry\/'
URL_FILTER = ("/favicon.ico", "/admin/jsi18n/")


class LoggingMiddleware(object):
    """Provides logging of logged in user interactions."""
    def process_response(self, request, response):
        """Log the actions of logged in users."""

        # Filter out the following paths.  Logs will not be created for these
        # paths.
        if re.match(MEDIA_REGEXP, request.path) or re.match(SENTRY_REGEXP,
            request.path) or request.path in URL_FILTER:
            return response

        log_mgr.write_log_entry(request=request, response=response)

        return response


@receiver(got_request_exception)
def log_request_exception(sender, **kwargs):
    """log the exception with traceback."""

    _ = sender
    exception = traceback.format_exc()
    request = kwargs["request"]
    log_mgr.write_log_entry(request=request, exception=exception)
