"""Alarm manager for scheduling and triggering alarms."""
import asyncio
import logging
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.util import dt as dt_util

from .alarm_storage import AlarmStorage
from .const import CONF_ALARM_SOUND, CONF_ALARM_VOLUME, CONF_MEDIA_PLAYER, DOMAIN

_LOGGER = logging.getLogger(__name__)


class AlarmManager:
    """Manages alarm scheduling and triggering."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the alarm manager."""
        self.hass = hass
        self.storage = AlarmStorage()
        self._scheduled_timers = {}
        self._running = False

    async def start(self):
        """Start the alarm manager and schedule all alarms."""
        if self._running:
            return

        self._running = True
        _LOGGER.info("Starting alarm manager")

        # Load and schedule all enabled alarms
        alarms = self.storage.get_enabled_alarms()
        for alarm in alarms:
            await self._schedule_alarm(alarm)

        _LOGGER.info("Alarm manager started with %d active alarms", len(alarms))

    async def stop(self):
        """Stop the alarm manager and cancel all scheduled alarms."""
        _LOGGER.info("Stopping alarm manager")
        self._running = False

        # Cancel all scheduled timers
        for timer_cancel in self._scheduled_timers.values():
            timer_cancel()
        self._scheduled_timers.clear()

    async def _schedule_alarm(self, alarm: dict):
        """Schedule a single alarm."""
        alarm_id = alarm["id"]
        time_str = alarm["time"]
        repeat_days = alarm.get("repeat_days")

        try:
            # Parse the alarm time
            hour, minute = map(int, time_str.split(":"))

            # Calculate next trigger time
            next_trigger = self._calculate_next_trigger(hour, minute, repeat_days)

            if next_trigger:
                # Schedule the alarm
                timer_cancel = async_track_point_in_time(
                    self.hass,
                    lambda now: self.hass.async_create_task(
                        self._trigger_alarm(alarm)
                    ),
                    next_trigger,
                )
                self._scheduled_timers[alarm_id] = timer_cancel
                _LOGGER.info(
                    "Scheduled alarm %d (%s) for %s",
                    alarm_id,
                    alarm["name"],
                    next_trigger,
                )

        except Exception as e:
            _LOGGER.error("Error scheduling alarm %d: %s", alarm_id, e)

    def _calculate_next_trigger(
        self, hour: int, minute: int, repeat_days: list[str] | None
    ) -> datetime | None:
        """Calculate the next trigger time for an alarm."""
        now = dt_util.now()
        today = now.date()

        # Create a datetime for today at the alarm time
        alarm_time = datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute))
        alarm_time = dt_util.as_local(alarm_time)

        if repeat_days:
            # Repeating alarm - find next occurrence
            day_map = {
                "mon": 0,
                "tue": 1,
                "wed": 2,
                "thu": 3,
                "fri": 4,
                "sat": 5,
                "sun": 6,
            }
            target_days = [day_map[day.lower()] for day in repeat_days if day.lower() in day_map]

            if not target_days:
                return None

            # Find the next day that matches
            for days_ahead in range(8):  # Check up to 7 days ahead + today
                check_date = today + timedelta(days=days_ahead)
                check_time = datetime.combine(
                    check_date, datetime.min.time().replace(hour=hour, minute=minute)
                )
                check_time = dt_util.as_local(check_time)

                if check_date.weekday() in target_days and check_time > now:
                    return check_time

            return None
        else:
            # One-time alarm
            if alarm_time > now:
                return alarm_time
            else:
                # If time has passed today, schedule for tomorrow
                tomorrow = today + timedelta(days=1)
                alarm_time = datetime.combine(
                    tomorrow, datetime.min.time().replace(hour=hour, minute=minute)
                )
                return dt_util.as_local(alarm_time)

    async def _trigger_alarm(self, alarm: dict):
        """Trigger an alarm (play sound, send notification, etc.)."""
        alarm_id = alarm["id"]
        alarm_name = alarm["name"]
        alarm_sound = alarm.get("sound", "default")

        _LOGGER.info("Triggering alarm %d: %s", alarm_id, alarm_name)

        try:
            # Track ringing alarm
            if DOMAIN not in self.hass.data:
                self.hass.data[DOMAIN] = {}
            if "ringing_alarms" not in self.hass.data[DOMAIN]:
                self.hass.data[DOMAIN]["ringing_alarms"] = []

            self.hass.data[DOMAIN]["ringing_alarms"].append(alarm_id)

            # Play alarm sound
            await self._play_alarm_sound(alarm_sound)

            # Send notification (optional)
            await self._send_notification(alarm_name, alarm_id)

            # If it's a one-time alarm, disable it
            if not alarm.get("repeat_days"):
                self.storage.toggle_alarm(alarm_id, False)
                _LOGGER.info("Disabled one-time alarm %d", alarm_id)
            else:
                # Reschedule repeating alarm for next occurrence
                await self._schedule_alarm(alarm)

        except Exception as e:
            _LOGGER.error("Error triggering alarm %d: %s", alarm_id, e)

    async def _play_alarm_sound(self, sound: str):
        """Play the alarm sound using a media player."""
        config_data = self.hass.data.get(DOMAIN, {}).get("config", {})
        media_player = config_data.get(CONF_MEDIA_PLAYER)
        volume = config_data.get(CONF_ALARM_VOLUME, 0.5)

        if not media_player:
            _LOGGER.warning("No media player configured for alarm sounds")
            return

        try:
            # Get custom file path if sound is "custom"
            if sound == "custom":
                custom_path = config_data.get("custom_sound_path")
                if custom_path:
                    sound_file = custom_path
                else:
                    sound_file = "/local/alarm_sounds/custom.mp3"
            else:
                # Map sound names to file paths or URLs
                sound_map = {
                    "default": "/local/alarm_sounds/default.mp3",
                    "gentle": "/local/alarm_sounds/gentle.mp3",
                    "beep": "/local/alarm_sounds/beep.mp3",
                    "chime": "/local/alarm_sounds/chime.mp3",
                    "bell": "/local/alarm_sounds/bell.mp3",
                }
                sound_file = sound_map.get(sound, sound_map["default"])

            # Set volume
            await self.hass.services.async_call(
                "media_player",
                "volume_set",
                {"entity_id": media_player, "volume_level": volume},
                blocking=True,
            )

            # Play sound
            await self.hass.services.async_call(
                "media_player",
                "play_media",
                {
                    "entity_id": media_player,
                    "media_content_id": sound_file,
                    "media_content_type": "music",
                },
                blocking=False,
            )

            _LOGGER.info("Playing alarm sound: %s on %s", sound, media_player)

        except Exception as e:
            _LOGGER.error("Error playing alarm sound: %s", e)

    async def _send_notification(self, alarm_name: str, alarm_id: int):
        """Send a notification for the alarm."""
        try:
            await self.hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "Alarm",
                    "message": f"Alarm '{alarm_name}' is ringing!",
                    "notification_id": f"alarm_{alarm_id}",
                },
                blocking=False,
            )
        except Exception as e:
            _LOGGER.error("Error sending alarm notification: %s", e)

    async def reschedule_all(self):
        """Reschedule all alarms (useful after configuration changes)."""
        _LOGGER.info("Rescheduling all alarms")

        # Cancel existing timers
        for timer_cancel in self._scheduled_timers.values():
            timer_cancel()
        self._scheduled_timers.clear()

        # Reload and reschedule
        alarms = self.storage.get_enabled_alarms()
        for alarm in alarms:
            await self._schedule_alarm(alarm)
