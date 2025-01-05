#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 jorgen <jorgen@jorgen-pc>
#
# Distributed under terms of the MIT license.
from os import path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,

    CONF_SERVER,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
)

async def async_setup_entry(hass, config):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(
            config,
            ["button", "switch"]
        )
    )

    return True
