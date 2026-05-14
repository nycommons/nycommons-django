from inplace_activity_stream.signals import action


def add_inplace_action(sender, verb, created=False, instance=None, **kwargs):
    if not instance or not created: return
    action.send(
        sender,
        verb=verb,
        action_object=instance, # action object, what was created
        place=instance.content_object.centroid, # where did it happen?
        target=instance.content_object, # what did it happen to?
        data={},
    )
