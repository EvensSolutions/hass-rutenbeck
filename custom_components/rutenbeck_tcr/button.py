"""Platform for IO Port integration."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

from . import DOMAIN
from .io_module import IOModule

async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
) -> None:
    module = IOModule(config)
    ports = await module.get_ports()

    async_add_entities(
        IOPort(module, port) for port in ports
    )

class IOPort(ButtonEntity):

    def __init__(self, module, port):
        super().__init__()

        self._module = module
        self._attr_name = port["name"]
        self._port_id = port["id"]
        self._impulse = port["impulse"]

    async def async_press(self) -> None:
        """Press the button"""
        await self._module.pulse(self._port_id, impulse=self._impulse)
