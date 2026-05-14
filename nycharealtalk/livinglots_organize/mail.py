from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string

from livinglots_mailsender.helpers import (mail_multiple_personalized,
                                           get_target_email_address)


def mass_mailing(subject, message, objects, template_name, **kwargs):
    messages = {}
    site = Site.objects.get_current()
    for obj in objects:
        # message gets sent once to each unique email address, thanks to dict
        messages[obj.email] = render_to_string(template_name, {
            'site': site,
            'target': obj.content_object,
            'message': message,
            'obj': obj,
        })

    # TODO optionally attach html version
    mail_multiple_personalized(subject, messages, **kwargs)


def mass_mail_watchers(subject, message, watchers, **kwargs):
    """
    Sends a message to watchers.
    """
    mass_mailing(
        subject,
        message,
        watchers,
        'livinglots/organize/notifications/mass_watcher_text.txt',
        **kwargs
    )


def mass_mail_organizers(subject, message, organizers, **kwargs):
    """
    Sends a message to organizers.
    """
    mass_mailing(
        subject,
        message,
        organizers,
        'livinglots/organize/notifications/mass_organizer_text.txt',
        **kwargs
    )


def mail_target_participants(participant_cls, target, subject,
                             excluded_emails=[], template=None,
                             html_template=None,
                             fail_silently_no_template=True, **kwargs):
    """Send a message to participants of a given target."""
    participants = participant_cls.objects.filter(
        content_type=ContentType.objects.get_for_model(target),
        object_id=target.pk,
    ).exclude(email=None)
    participants = [p for p in participants if p.email not in excluded_emails]
    messages = _get_messages(participants, template,
                             fail_silently_no_template=fail_silently_no_template,
                             **kwargs)
    html_messages = None
    if html_template:
        html_messages = _get_messages(participants, html_template,
                                      fail_silently_no_template=True, **kwargs)
    mail_multiple_personalized(subject, messages, html_messages=html_messages,
                               from_email=get_target_email_address(target))


def get_target_participant_context(participant, obj, **kwargs):
    """Get context for targetted notification emails."""
    context = kwargs
    context.update({
        'BASE_URL': Site.objects.get_current().domain,
        'MAILREADER_REPLY_PREFIX': settings.MAILREADER_REPLY_PREFIX,
        'obj': obj,
        'participant': participant,
        'target': participant.content_object,
    })
    return context


def _get_messages(participants, template_name, fail_silently_no_template=False,
                  obj=None, **kwargs):
    messages = {}
    for p in participants:
        context = get_target_participant_context(p, obj, **kwargs)
        try:
            messages[p.email] = render_to_string(template_name, context)
        except TemplateDoesNotExist:
            if fail_silently_no_template:
                continue
            else:
                raise
    return messages
