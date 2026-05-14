from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from livinglots_mailsender.helpers import (mail_multiple_personalized,
                                           get_target_email_address)


def mail_facilitators(target, subject, excluded_emails=[],
                      template='organize/notifications/facilitators_text.txt',
                      html_template=None, **kwargs):
    """Sends a message to facilitators."""
    facilitators = settings.FACILITATORS['global']
    facilitators = [f for f in facilitators if f not in excluded_emails]

    kwargs['target'] = target
    messages = _get_facilitator_messages(facilitators, template, **kwargs)
    try:
        html_messages = _get_facilitator_messages(facilitators, html_template,
                fail_silently_no_template=True, **kwargs)
    except Exception:
        html_messages = None
    mail_multiple_personalized(subject, messages, fail_silently=False,
                               html_messages=html_messages,
                               from_email=get_target_email_address(target))


def _get_facilitator_messages(facilitators, template_name, **kwargs):
    messages = {}
    for facilitator in facilitators:
        context = kwargs
        context.update({
            'BASE_URL': Site.objects.get_current().domain,
            'MAILREADER_REPLY_PREFIX': settings.MAILREADER_REPLY_PREFIX,
        })
        messages[facilitator] = render_to_string(template_name, context)
    return messages
