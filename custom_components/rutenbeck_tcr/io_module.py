import aiohttp
import asyncio
import re
from pyquery import PyQuery

from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    DOMAIN,

    CONF_SERVER,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
)

class IOModule:

    def __init__(self, config):
        self._server = config.data.get(CONF_SERVER)
        self._port = config.data.get(CONF_PORT)

        self._username = config.data.get(CONF_USERNAME)
        self._password = config.data.get(CONF_PASSWORD)

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

    async def pulse(self, id, impulse="00:00:01", state="on"):
        command = "normal" if state == "on" else "reset"
        url = self.server_url('/impl.cgi?ausg' + str(id) + impulse + command)
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
        return DeviceInfo(
            identifiers={
                (DOMAIN, self._server)
            },
            name=self._server,
        )
