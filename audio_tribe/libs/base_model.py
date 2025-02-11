from __future__ import annotations

from collections.abc import Iterable

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseAbstractModel(models.Model):
    created_datetime = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_datetime = models.DateTimeField(_("Last update at"), auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        """Override save for triggering updated_datetime on update_fields case."""
        listed_for_update_fields = None
        if update_fields:
            listed_for_update_fields = list(update_fields)
            listed_for_update_fields.append("updated_datetime")

        return super().save(
            force_insert, force_update, using, listed_for_update_fields or None
        )
