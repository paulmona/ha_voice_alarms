"""
Constants for the Alarm Assistant custom component.

This module defines configuration keys and domain names for alarm management.
"""

DOMAIN = "alarm_assistant"
ADDON_NAME = "Voice Alarm Assistant"

ALARM_API_NAME = "Alarm Management"

ALARM_SERVICES_PROMPT = """
You have access to alarm management tools to help users set, list, and delete alarms.
- When a user asks to set an alarm, use the set_alarm tool
- When a user asks what alarms are set, use the list_alarms tool
- When a user asks to delete or cancel an alarm, use the delete_alarm tool
- When a user asks to stop or dismiss a ringing alarm, use the stop_alarm tool
- When a user asks to snooze a ringing alarm, use the snooze_alarm tool
You also have access to timer tools:
- When a user asks to set a timer, use the set_timer tool
- When a user asks what timers are running, use the list_timers tool
- When a user asks to cancel a timer, use the cancel_timer tool
- When a user asks to stop a timer, use the cancel_timer tool
""".strip()

# Configuration constants
CONF_ALARM_ENABLED = "alarm_enabled"
CONF_ALARM_SOUND = "alarm_sound"
CONF_ALARM_VOLUME = "alarm_volume"
CONF_MEDIA_PLAYER = "media_player_entity"

# Service defaults
SERVICE_DEFAULTS = {
    CONF_ALARM_VOLUME: 0.5,
    CONF_ALARM_SOUND: "default",
    CONF_MEDIA_PLAYER: None,
}

# Alarm sound options
ALARM_SOUNDS = [
    "default",
    "gentle",
    "beep",
    "chime",
    "bell",
    "custom",
]

# Timer constants
CONF_TIMER_ENABLED = "timer_enabled"
CONF_TIMER_SOUND = "timer_sound"

# Snooze settings
CONF_SNOOZE_DURATION = "snooze_duration"
DEFAULT_SNOOZE_DURATION = 9  # minutes
