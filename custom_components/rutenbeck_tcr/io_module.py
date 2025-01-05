import aiohttp
import asyncio
import re
from pyquery import PyQuery

from datetime import timedelta
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .logger import logger
from .const import (
    DOMAIN,

    CONF_SERVER,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
)

class IOModule(DataUpdateCoordinator):

    module_cache = {}

    def from_config(hass, config):
        server = config.data.get(CONF_SERVER)
        port = config.data.get(CONF_PORT)
        name = "%s:%s" % (server, port)
        cache = IOModule.module_cache

        if not name in cache:
            cache[name] = IOModule(hass, config)

        return cache[name]

    def __init__(self, hass, config):
        server = config.data.get(CONF_SERVER)
        port = config.data.get(CONF_PORT)

        name = "%s:%s" % (server, port)

        super().__init__(
            hass,
            logger,
            name=name,
            update_interval=timedelta(seconds=15)
        )

        self.name = name
        self._server = server
        self._port = port

        self._username = config.data.get(CONF_USERNAME)
        self._password = config.data.get(CONF_PASSWORD)

        self._device = self._create_device()

    def _create_device(self):
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.name)
            },
            name=self.name,
        )

    async def _async_setup(self):
        pass

    async def _async_update_data(self):
        return await self.get_status()

    def server_url(self, path=""):
        return 'http://' + self._server + ':' + str(self._port) + path

    async def get_ports(self):
        url = self.server_url()
        py = PyQuery(await self.get(url))

        ports = py('form > div > table input[type=button]')

        def build_port(block):
            name = block('td[align=center]').text()
            impulse = block('input[type=text]').attr('value')
            js_handler = block('input[type=button]').attr('onclick')
            id = re.sub('^[^(]+\((\d+)\)$', '\g<1>', js_handler)

            return { "id": id, "name": name, "impulse": impulse }

        return [ build_port(py(p).parents('.tab1')) for p in ports ]

    async def get_status(self):
        try:
            url = self.server_url('/status.xml')
            py = PyQuery(await self.get(url))

            response = py('response > *')
            status = {}

            for led in response.items():
                led = led[0]
                if led.tag.startswith('led'):
                    tag_name = led.tag.replace('led', '')
                    status[tag_name] = (led.text == "1")

            return status
        except Exception as e:
            logger.error("Failed to get status", e)
            return {}

    async def pulse(self, id, impulse="00:00:01", state="on"):
        command = "normal" if state == "on" else "reset"
        url = self.server_url('/impl.cgi?ausg' + str(id) + impulse + command)
        await self.post(url)

    async def turn_on(self, id):
        await self.toggle(id, "on")

    async def turn_off(self, id):
        await self.toggle(id, "off")

    async def toggle(self, id, state):
        state = "Aus" if state == "off" else "Ein"
        url = self.server_url('/leds.cgi?led=' + str(id) + '&value=' + state)
        await self.post(url)

    async def get(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, auth=self.basic_auth()) as resp:
                return await resp.text(encoding="ISO-8859-1")

    async def post(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, auth=self.basic_auth()) as resp:
                pass

    def basic_auth(self):
        return aiohttp.BasicAuth(
            self._username,
            self._password
        )

    @property
    def device_info(self):
        return self._device
