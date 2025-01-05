from homeassistant.core import callback
from homeassistant.components.button import ButtonEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import generate_entity_id

class IOPort(CoordinatorEntity, ButtonEntity, SwitchEntity):

    def __init__(self, module, port, hass=None):
        port_id = port["id"]

        super().__init__(module, context=port_id)

        self._module = module
        self._port_id = port_id
        self._impulse = port["impulse"]

        self.is_on = None
        self.should_poll = True
        self.name = port["name"]

        unique_id = "%s.%s" % (module.name, self.name)
        self.unique_id = generate_entity_id("{}", unique_id, hass=hass)

        self.state = False

    @property
    def device_info(self):
        return self._module.device_info

    @callback
    def _handle_coordinator_update(self) -> None:
        status = self._module.data

        if self._port_id in status:
            self.is_on = status[self._port_id]
            self.state = "on" if self.is_on else "off"
        else:
            self.is_on = None
            self.state = None

        #  self.async_write_ha_state()

    async def async_press(self) -> None:
        """Pulse the button"""
        await self._module.pulse(self._port_id, impulse=self._impulse)

    async def async_turn_off(self) -> None:
        """Turn on IO port"""
        await self._module.turn_off()

    async def async_turn_on(self) -> None:
        """Turn off IO Port"""
        await self._module.turn_on()
