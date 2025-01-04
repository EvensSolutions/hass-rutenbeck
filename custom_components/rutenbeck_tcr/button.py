"""Platform for IO Port integration."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity import generate_entity_id

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
        [ IOPort(module, port, hass=hass) for port in ports ]
    )

class IOPort(ButtonEntity):

    def __init__(self, module, port, hass=None):
        super().__init__()

        self._module = module
        self._port_id = port["id"]
        self._impulse = port["impulse"]

        self.name = port["name"]

        unique_id = "%s.%s" % (module._server, self.name)
        self.unique_id = generate_entity_id("button.{}", unique_id, hass=hass)

    @property
    def device_info(self):
        return self._module.device_info

    async def async_press(self) -> None:
        """Press the button"""
        await self._module.pulse(self._port_id, impulse=self._impulse)
