"""LLM function implementations for alarm services."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import llm

from .alarm_control_tools import SnoozeAlarmTool, StopAlarmTool
from .alarm_tools import DeleteAlarmTool, ListAlarmsTool, SetAlarmTool
from .const import (
    ALARM_API_NAME,
    ALARM_SERVICES_PROMPT,
    CONF_ALARM_ENABLED,
    CONF_TIMER_ENABLED,
    DOMAIN,
)
from .timer_tools import CancelTimerTool, ListTimersTool, SetTimerTool

_LOGGER = logging.getLogger(__name__)


class AlarmAPI(llm.API):
    """Alarm management API for LLM integration."""

    def __init__(self, hass: HomeAssistant, name: str) -> None:
        """Initialize the API."""
        super().__init__(hass=hass, id=DOMAIN, name=name)

    def get_enabled_tools(self) -> list:
        """Get the list of enabled alarm and timer tools."""
        config_data = self.hass.data[DOMAIN].get("config", {})
        entry = next(iter(self.hass.config_entries.async_entries(DOMAIN)), None)
        if entry:
            config_data = {**config_data, **entry.options}

        tools = []
        alarm_enabled = config_data.get(CONF_ALARM_ENABLED, True)
        timer_enabled = config_data.get(CONF_TIMER_ENABLED, True)

        if alarm_enabled:
            tools.extend([
                SetAlarmTool(),
                ListAlarmsTool(),
                DeleteAlarmTool(),
                StopAlarmTool(),
                SnoozeAlarmTool(),
            ])

        if timer_enabled:
            tools.extend([
                SetTimerTool(),
                ListTimersTool(),
                CancelTimerTool(),
            ])

        return tools

    async def async_get_api_instance(
        self, llm_context: llm.LLMContext
    ) -> llm.APIInstance:
        """Get API instance."""
        return llm.APIInstance(
            api=self,
            api_prompt=ALARM_SERVICES_PROMPT,
            llm_context=llm_context,
            tools=self.get_enabled_tools(),
        )


async def setup_llm_functions(hass: HomeAssistant, config_data: dict[str, Any]) -> None:
    """Set up LLM functions for alarm services."""
    # Check if already set up with same config to avoid unnecessary work
    if (
        DOMAIN in hass.data
        and "api" in hass.data[DOMAIN]
        and hass.data[DOMAIN].get("config") == config_data
    ):
        return

    # Only clean up if we already have an API registered
    if DOMAIN in hass.data and "api" in hass.data[DOMAIN]:
        await cleanup_llm_functions(hass)

    # Store API instance and config in hass.data
    hass.data.setdefault(DOMAIN, {})
    alarm_api = AlarmAPI(hass, ALARM_API_NAME)

    hass.data[DOMAIN]["api"] = alarm_api
    hass.data[DOMAIN]["config"] = config_data.copy()

    # Register the API with Home Assistant's LLM system
    try:
        if alarm_api.get_enabled_tools():
            unregister_func = llm.async_register_api(hass, alarm_api)
            hass.data[DOMAIN]["unregister_api"] = unregister_func
            _LOGGER.info("Alarm Assistant API registered with LLM system")
    except Exception as e:
        _LOGGER.error("Failed to register LLM API: %s", e)
        raise


async def cleanup_llm_functions(hass: HomeAssistant) -> None:
    """Clean up LLM functions."""
    if DOMAIN in hass.data:
        # Unregister API if we have the unregister function
        unreg_func = hass.data[DOMAIN].get("unregister_api")
        if unreg_func:
            try:
                unreg_func()
                _LOGGER.info("Alarm Assistant API unregistered from LLM system")
            except Exception as e:
                _LOGGER.debug("Error unregistering LLM API: %s", e)

        # Clean up stored data (but keep alarm manager and storage)
        hass.data[DOMAIN].pop("api", None)
        hass.data[DOMAIN].pop("unregister_api", None)
        hass.data[DOMAIN].pop("config", None)
