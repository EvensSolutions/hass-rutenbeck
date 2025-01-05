"""Platform for IO Port integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity import generate_entity_id

from . import DOMAIN
from .io_module import IOModule
from .io_port import IOPort

async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
) -> None:
    module = IOModule.from_config(hass, config)
    ports = await module.get_ports()

    async_add_entities(
        [ IOPort(module, port, hass=hass) for port in ports ]
    )
