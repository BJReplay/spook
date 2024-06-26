"""Spook - Your homie."""

from __future__ import annotations

from typing import TYPE_CHECKING

import voluptuous as vol

from homeassistant.components.homeassistant import DOMAIN
from homeassistant.helpers import area_registry as ar, config_validation as cv

from ....services import AbstractSpookAdminService

if TYPE_CHECKING:
    from homeassistant.core import ServiceCall


class SpookService(AbstractSpookAdminService):
    """Home Assistant service to remove a label from an area."""

    domain = DOMAIN
    service = "remove_label_from_area"
    schema = {
        vol.Required("label_id"): vol.All(cv.ensure_list, [cv.string]),
        vol.Required("area_id"): vol.All(cv.ensure_list, [cv.string]),
    }

    async def async_handle_service(self, call: ServiceCall) -> None:
        """Handle the service call."""
        area_registry = ar.async_get(self.hass)
        for area_id in call.data["area_id"]:
            if area_entry := area_registry.async_get(area_id):
                labels = area_entry.labels.copy()
                labels.difference_update(call.data["label_id"])
                area_registry.async_update(area_id, labels=labels)
