"""LLM Tools for controlling ringing alarms (stop, snooze)."""
import logging
from datetime import datetime, timedelta

import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers import llm
from homeassistant.util.json import JsonObjectType

from .const import CONF_SNOOZE_DURATION, DEFAULT_SNOOZE_DURATION, DOMAIN

_LOGGER = logging.getLogger(__name__)


class StopAlarmTool(llm.Tool):
    """Tool for stopping a ringing alarm."""

    name = "stop_alarm"
    description = "Stop or dismiss a currently ringing alarm. Use this when the user wants to turn off an alarm that is currently sounding. This stops the alarm sound immediately."
    response_instruction = """
    Confirm to the user that the alarm has been stopped.
    Keep your response concise and friendly, in plain text without formatting.
    """

    parameters = vol.Schema({})

    def wrap_response(self, response: dict) -> dict:
        response["instruction"] = self.response_instruction
        return response

    async def async_call(
        self,
        hass: HomeAssistant,
        tool_input: llm.ToolInput,
        llm_context: llm.LLMContext,
    ) -> JsonObjectType:
        """Call the tool to stop ringing alarm."""
        _LOGGER.info("Stopping ringing alarm")

        try:
            # Get ringing alarms from hass.data
            ringing_alarms = hass.data.get(DOMAIN, {}).get("ringing_alarms", [])

            if not ringing_alarms:
                return {"error": "No alarm is currently ringing"}

            # Stop all ringing alarms
            count = 0
            for alarm_id in ringing_alarms[:]:  # Copy list to modify during iteration
                await self._stop_alarm(hass, alarm_id)
                count += 1

            # Clear ringing alarms list
            if DOMAIN in hass.data:
                hass.data[DOMAIN]["ringing_alarms"] = []

            return self.wrap_response(
                {
                    "success": True,
                    "count": count,
                    "message": f"Stopped {count} ringing alarm{'s' if count != 1 else ''}",
                }
            )

        except Exception as e:
            _LOGGER.error("Error stopping alarm: %s", e)
            return {"error": f"Failed to stop alarm: {e!s}"}

    async def _stop_alarm(self, hass: HomeAssistant, alarm_id: int):
        """Stop a specific alarm."""
        # Cancel auto-dismiss timer if it exists
        alarm_manager = hass.data.get(DOMAIN, {}).get("alarm_manager")
        if alarm_manager and hasattr(alarm_manager, "_auto_dismiss_timers"):
            cancel_func = alarm_manager._auto_dismiss_timers.pop(alarm_id, None)
            if cancel_func:
                cancel_func()
                _LOGGER.debug("Cancelled auto-dismiss timer for alarm %d", alarm_id)

        # Stop media player
        config_data = hass.data.get(DOMAIN, {}).get("config", {})
        media_player = config_data.get("media_player_entity")

        if media_player:
            try:
                await hass.services.async_call(
                    "media_player",
                    "media_stop",
                    {"entity_id": media_player},
                    blocking=False,
                )
            except Exception as e:
                _LOGGER.warning("Could not stop media player: %s", e)

        # Dismiss notification
        try:
            await hass.services.async_call(
                "persistent_notification",
                "dismiss",
                {"notification_id": f"alarm_{alarm_id}"},
                blocking=False,
            )
        except Exception as e:
            _LOGGER.warning("Could not dismiss notification: %s", e)


class SnoozeAlarmTool(llm.Tool):
    """Tool for snoozing a ringing alarm."""

    name = "snooze_alarm"
    description = "Snooze a currently ringing alarm. The alarm will stop now and ring again after the snooze duration (default 9 minutes). Use this when the user wants to sleep a bit longer."
    response_instruction = """
    Confirm to the user that the alarm has been snoozed and when it will ring again.
    Keep your response concise and friendly, in plain text without formatting.
    """

    parameters = vol.Schema(
        {
            vol.Optional(
                "duration_minutes",
                description="How many minutes to snooze for. Default is 9 minutes if not specified.",
            ): int,
        }
    )

    def wrap_response(self, response: dict) -> dict:
        response["instruction"] = self.response_instruction
        return response

    async def async_call(
        self,
        hass: HomeAssistant,
        tool_input: llm.ToolInput,
        llm_context: llm.LLMContext,
    ) -> JsonObjectType:
        """Call the tool to snooze ringing alarm."""
        duration_minutes = tool_input.tool_args.get("duration_minutes")

        # Get snooze duration from config or use default
        if duration_minutes is None:
            config_data = hass.data.get(DOMAIN, {}).get("config", {})
            duration_minutes = config_data.get(
                CONF_SNOOZE_DURATION, DEFAULT_SNOOZE_DURATION
            )

        _LOGGER.info("Snoozing alarm for %d minutes", duration_minutes)

        try:
            # Get ringing alarms from hass.data
            ringing_alarms = hass.data.get(DOMAIN, {}).get("ringing_alarms", [])

            if not ringing_alarms:
                return {"error": "No alarm is currently ringing"}

            # Cancel auto-dismiss timers for all ringing alarms
            alarm_manager = hass.data[DOMAIN].get("alarm_manager")
            if alarm_manager and hasattr(alarm_manager, "_auto_dismiss_timers"):
                for alarm_id in ringing_alarms:
                    cancel_func = alarm_manager._auto_dismiss_timers.pop(alarm_id, None)
                    if cancel_func:
                        cancel_func()
                        _LOGGER.debug("Cancelled auto-dismiss timer for alarm %d during snooze", alarm_id)

            # Stop the sound
            config_data = hass.data.get(DOMAIN, {}).get("config", {})
            media_player = config_data.get("media_player_entity")

            if media_player:
                try:
                    await hass.services.async_call(
                        "media_player",
                        "media_stop",
                        {"entity_id": media_player},
                        blocking=False,
                    )
                except Exception as e:
                    _LOGGER.warning("Could not stop media player: %s", e)

            # Schedule alarm to ring again after snooze duration
            from homeassistant.helpers.event import async_call_later

            count = 0

            for alarm_id in ringing_alarms[:]:
                # Get alarm details
                from .alarm_storage import AlarmStorage
                storage = AlarmStorage()
                alarms = storage.get_all_alarms()
                alarm = next((a for a in alarms if a["id"] == alarm_id), None)

                if alarm:
                    # Schedule snooze callback
                    async def snooze_callback(now, aid=alarm_id):
                        if alarm_manager:
                            # Re-trigger the alarm
                            await alarm_manager._trigger_alarm(
                                {"id": aid, "name": f"Snoozed: {alarm['name']}",
                                 "sound": alarm.get("sound", "default")}
                            )

                    async_call_later(
                        hass, duration_minutes * 60, snooze_callback
                    )
                    count += 1

            # Clear ringing alarms list and dismiss notifications
            if DOMAIN in hass.data:
                hass.data[DOMAIN]["ringing_alarms"] = []

            for alarm_id in ringing_alarms:
                try:
                    await hass.services.async_call(
                        "persistent_notification",
                        "dismiss",
                        {"notification_id": f"alarm_{alarm_id}"},
                        blocking=False,
                    )
                except Exception as e:
                    _LOGGER.warning("Could not dismiss notification: %s", e)

            # Calculate when alarm will ring again
            snooze_until = datetime.now() + timedelta(minutes=duration_minutes)
            snooze_time = snooze_until.strftime("%H:%M")

            return self.wrap_response(
                {
                    "success": True,
                    "count": count,
                    "duration_minutes": duration_minutes,
                    "snooze_until": snooze_time,
                    "message": f"Snoozed {count} alarm{'s' if count != 1 else ''} for {duration_minutes} minutes. Will ring again at {snooze_time}",
                }
            )

        except Exception as e:
            _LOGGER.error("Error snoozing alarm: %s", e)
            return {"error": f"Failed to snooze alarm: {e!s}"}
