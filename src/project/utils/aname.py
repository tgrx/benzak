from functools import singledispatch
from typing import Text

from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.query_utils import DeferredAttribute


@singledispatch
def aname(obj) -> Text:
    return obj


@aname.register
def _(obj: DeferredAttribute) -> Text:
    return obj.field_name


@aname.register
def _(obj: ForwardManyToOneDescriptor) -> Text:
    return obj.field.name
