"""
Template tags for the notes app, loosely based on django.contrib.comments.

"""
from django import template

from livinglots_generictags.tags import (GetGenericRelationList,
                                         RenderGenericRelationList,
                                         GetGenericRelationCount)

from ..models import Note

register = template.Library()


class RenderNoteList(RenderGenericRelationList):
    model = Note

    def get_objects(self, target):
        return super(RenderNoteList, self).get_objects(target).order_by('-added')

register.tag(RenderNoteList)


class GetNoteList(GetGenericRelationList):
    model = Note

register.tag(GetNoteList)


class GetNoteCount(GetGenericRelationCount):
    model = Note

register.tag(GetNoteCount)
