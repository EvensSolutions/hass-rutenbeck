from homeassistant import config_entries
import voluptuous as vol

from .const import (
    DOMAIN,
    INTEGRATION_NAME,

    CONF_SERVER,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD
)

class SelfhostedCloudFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow"""

    async def async_step_user(self, info):
        if info is not None:
            return self.async_create_entry(
                title=INTEGRATION_NAME,
                data=info
            )
            pass

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_SERVER): str,
                vol.Optional(CONF_PORT): int,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            })
        )
